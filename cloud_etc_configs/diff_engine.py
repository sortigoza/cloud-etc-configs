from functools import partial
from pprint import pprint
from typing import Dict, List, Set

from cloud_etc_configs.entities import PlanDiff, Remotekey, ServiceConfiguration


def dummy_diff(
    current_states: List[str],
    all_existing_parameters: List[Remotekey],
    env_services_configurations: List[ServiceConfiguration],
):
    """
    return a list of dicts with the service config reference and
    the diff of RemoteKeys that needs to be updated
    """
    res = []
    for config in env_services_configurations:
        res.append({"service_configuration": config, "diff": config.configurations})
    return res


# Compute the Diff
# things we need to check here:
# - is it a new parameter? -> create: check existing parameters vs env_configs
# - is it an existing parameter? -> update: check existing parameters vs env_configs
# - was a parameter deleted? -> delete: check existing parameters and current_state (we manage this param) vs env_configs
def compute_diff(
    current_states: Dict[str, str],
    all_existing_parameters: List[Remotekey],
    env_services_configurations: List[ServiceConfiguration],
):
    all_existing_parameters_kv_set = set(
        f"{x.key}/{x.value}" for x in all_existing_parameters
    )
    all_existing_parameters_k_set = set(x.key for x in all_existing_parameters)

    service_diff = partial(
        compute_service_diff,
        all_existing_parameters_kv_set,
        all_existing_parameters_k_set,
    )
    diffs = []
    for service in env_services_configurations:
        current_diff = service_diff(set(current_states[service.service_name]), service)
        diffs.append({"service_configuration": service, "diff": current_diff})
    return diffs


def compute_service_diff(
    all_existing_parameters_kv_set: Set[str],
    all_existing_parameters_k_set: Set[str],
    current_states_set: Set[str],
    env_config: ServiceConfiguration,
):
    res_diff = PlanDiff.new_with_mutable_defaults()
    keys = set([])
    for parameter in env_config.configurations:
        key = parameter.key
        # store the key for later
        keys.add(key)
        kv_set_key = f"{parameter.key}/{parameter.value}"
        # the key is not present in exisitng parameters
        if key not in all_existing_parameters_k_set:
            res_diff.create.append(parameter)
        # the key and value are present in existing parameters
        elif kv_set_key in all_existing_parameters_kv_set:
            res_diff.ok.append(parameter)
        # the key is present but since it dind't match the value (previous if)
        # it is differetn.
        elif key in all_existing_parameters_k_set:
            res_diff.update.append(parameter)

    # check keys that are present in the state but not in the config
    keys_to_delete = current_states_set - keys
    for key in keys_to_delete:
        res_diff.delete.append(Remotekey(key=key, value=""))

    return res_diff
