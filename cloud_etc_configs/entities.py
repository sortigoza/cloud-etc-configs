from __future__ import annotations

# from pydantic import BaseModel
import re
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Configuration:
    config_file_name: str
    config_file_path: str
    base_path: str
    remote_base_key: str
    environment: str
    common: str
    parameter_storage: str


@dataclass
class Remotekey:
    key: str
    value: str


@dataclass
class PlanDiff:
    ok: List
    create: List
    update: List
    delete: List

    @staticmethod
    def new_with_mutable_defaults():
        return PlanDiff(
            ok=[],
            create=[],
            update=[],
            delete=[],
        )


@dataclass
class ServiceConfiguration:
    environment: str
    service_name: str
    path: str
    remote_state_path: str
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
    def from_raw_data(raw_configuration, path, environment, remote_base_key):
        service_name = raw_configuration["service_name"]
        configurations = ServiceConfiguration._build_keys(
            remote_base_key, service_name, raw_configuration["configuration"]
        )
        return ServiceConfiguration(
            environment=environment,
            path=path,
            service_name=service_name,
            remote_state_path=f"{remote_base_key}/{service_name}/state-metadata",
            configurations=configurations,
        )

    @staticmethod
    def _build_keys(remote_base_key, service_name, keys_dict):
        def remote_key(param_name):
            return f"{remote_base_key}/{service_name}/{param_name}"

        return [Remotekey(key=remote_key(k), value=v) for k, v in keys_dict.items()]