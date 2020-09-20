from __future__ import annotations
from typing import Optional, List
import re
from dataclasses import dataclass


@dataclass
class Configuration:
    remote_store_type: str = "ssm"
    base_path: str = "/saul-test"
    target_environment: str = "development"


@dataclass
class Remotekey:
    key: str
    value: str


@dataclass
class ServiceConfiguration:
    environment: str
    service_name: str
    path: str
    remote_state_path: str
    kv_path: str
    configurations: List[Remotekey]

    def add_common_keys(self, configuration: Optional[ServiceConfiguration]):
        if configuration is None:
            return self

        common_configs = {x.key: x.value for x in configuration.configurations}
        self_configs = {x.key: x.value for x in self.configurations}
        new_configs = {**common_configs, **self_configs}
        self.configurations = [
            Remotekey(key=k, value=v) for k, v in new_configs.items()
        ]
        return self

    def get_state(self):
        return [x.key for x in self.configurations]

    @staticmethod
    def from_path_and_data(path, raw_configuration, remote_base_path):
        match = re.search(r"environment/(.*)/(.*)\.yaml", path, re.I)
        if match:
            environment = match.group(1)
            service_name = match.group(2)
        assert service_name == raw_configuration["service_name"]
        configurations = ServiceConfiguration._build_keys(
            remote_base_path, service_name, raw_configuration["configuration"]
        )
        return ServiceConfiguration(
            environment=environment,
            path=path,
            service_name=service_name,
            kv_path=service_name,
            remote_state_path=f"{remote_base_path}/{service_name}/state-metadata",
            configurations=configurations,
        )

    @staticmethod
    def _build_keys(remote_base_path, service_name, keys_dict):
        def remote_key(param_name):
            return f"{remote_base_path}/{service_name}/{param_name}"

        return [Remotekey(key=remote_key(k), value=v) for k, v in keys_dict.items()]
