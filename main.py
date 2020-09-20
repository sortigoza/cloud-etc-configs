from automation.sync_task import SyncTask


task = SyncTask()
task.execute()

# import operator
# from itertools import groupby
# from functools import reduce
# from typing import List

# from pprint import pprint
# from automation.diff_engine import compute_diff, dummy_diff
# from automation.loader import load_configurations
# from automation.entities import (
#     ServiceConfiguration,
#     Remotekey,
#     Configuration,
# )
# from automation.adapters import get_remote_handler


# def get_common_and_envs(all_envs):
#     common = None
#     environments = []
#     for i in all_envs:
#         if i.environment == "common":
#             common = i
#         else:
#             environments.append(i)

#     return common, environments


# config = Configuration()
# remote_handler = get_remote_handler(config.remote_store_type, config.base_path)

# # Load local configurations for the target env
# grouped_by_service_name = load_configurations(config)

# # Combine with the common configurations
# env_services_configurations = []
# for k, v in grouped_by_service_name.items():
#     common, environment_services = get_common_and_envs(v)
#     env_services_configurations += [
#         x.add_common_keys(common) for x in environment_services
#     ]

# # Get remote configuration state
# all_existing_parameters = remote_handler.get_all_parameters()
# current_states = reduce(
#     lambda acc, x: {**acc, **{x.service_name: remote_handler.get_current_state(x)}},
#     env_services_configurations,
#     {},
# )
# pprint(all_existing_parameters)

# # Compute the Diff
# parameters_diff = compute_diff(
#     current_states, all_existing_parameters, env_services_configurations
# )
# pprint(parameters_diff)

# # Update the Diff and Update apply metadata, skip if dry-run
# for service_with_diff in parameters_diff:
#     current_plan = service_with_diff["diff"]
#     for parameter in current_plan["create"] + current_plan["update"]:
#         remote_handler.update_key(parameter.key, parameter.value)
#     for parameter in current_plan["delete"]:
#         remote_handler.delete_key(parameter.key)
#     remote_handler.write_state(service_with_diff["service_configuration"])
