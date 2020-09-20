import dataclasses
import operator
from dataclasses import dataclass
from functools import partial, reduce
from itertools import groupby
from pprint import pformat, pprint
from typing import List

from toolz.functoolz import pipe

from cloud_etc_configs.adapters import get_remote_handler
from cloud_etc_configs.diff_engine import compute_diff, dummy_diff
from cloud_etc_configs.entities import Configuration, Remotekey, ServiceConfiguration
from cloud_etc_configs.loader import load_services_configurations, load_tool_config
from cloud_etc_configs.logger import get_logger

logger = get_logger()


@dataclass
class DiffInput:
    current_states: List[str]
    all_existing_parameters: List[Remotekey]
    env_services_configurations: List[ServiceConfiguration]


class SyncTask:
    def _get_common_and_envs(self, all_envs):
        common = None
        environments = []
        for i in all_envs:
            if i.environment == "common":
                common = i
            else:
                environments.append(i)

        return common, environments

    def execute(self):
        self.config = load_tool_config(base_path="./environment/development")
        self.remote_handler = get_remote_handler(
            self.config.parameter_storage, self.config.remote_base_key
        )

        pipe(
            load_services_configurations(self.config),
            partial(self.print_state, "all_services_configurations"),
            self.combine_with_common_configurations,
            partial(self.print_state, "env_services_configurations"),
            self.get_remote_configuration_state,
            self.compute_the_diff,
            self.print_diff,
            self.apply_the_diff_with_metadata,
        )

    def combine_with_common_configurations(self, grouped_by_service_name):
        env_services_configurations = []
        for _, v in grouped_by_service_name.items():
            common, environment_services = self._get_common_and_envs(v)
            env_services_configurations += [
                x.add_common_keys(common) for x in environment_services
            ]
        return env_services_configurations

    def get_remote_configuration_state(self, env_services_configurations):
        all_existing_parameters = self.remote_handler.get_all_parameters()
        current_states = reduce(
            lambda acc, x: {
                **acc,
                **{x.service_name: self.remote_handler.get_current_state(x)},
            },
            env_services_configurations,
            {},
        )
        return DiffInput(
            current_states=current_states,
            all_existing_parameters=all_existing_parameters,
            env_services_configurations=env_services_configurations,
        )

    def compute_the_diff(self, diff_input: DiffInput):
        return compute_diff(
            diff_input.current_states,
            diff_input.all_existing_parameters,
            diff_input.env_services_configurations,
        )

    def apply_the_diff_with_metadata(self, parameters_diff):
        # Update the Diff and Update apply metadata, skip if dry-run
        for service_with_diff in parameters_diff:
            current_plan = service_with_diff["diff"]
            for parameter in current_plan.create + current_plan.update:
                self.remote_handler.update_key(parameter.key, parameter.value)
            for parameter in current_plan.delete:
                self.remote_handler.delete_key(parameter.key)
            self.remote_handler.write_state(service_with_diff["service_configuration"])

    def print_state(self, message, value):
        if dataclasses.is_dataclass(value):
            logger.info("%s: \n%s", message, pformat(dataclasses.asdict(value)))
        elif isinstance(value, list) or isinstance(value, dict):
            logger.info("%s: \n%s", message, pformat(value))
        else:
            logger.info("%s: %s", message, value)

        return value

    def print_diff(self, diffs_list):
        for x in diffs_list:
            pprint(
                {
                    "service_name": x["service_configuration"].service_name,
                    "diff": dataclasses.asdict(x["diff"]),
                }
            )
        return diffs_list
