import operator
import os
import re
from dataclasses import asdict
from glob import glob
from itertools import groupby
from typing import Dict

import yaml

from cloud_etc_configs.entities import Configuration, ServiceConfiguration
from cloud_etc_configs.logger import get_logger

logger = get_logger()


def _read_yaml_to_dict(file_path) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f.read())


def _get_etc_files(config: Configuration):
    return [
        x
        for x in glob(f"{config.base_path}/**/*.yaml", recursive=True)
        if not re.match(f".*/{config.config_file_name}", x, re.I)
    ]


def _get_etc_common_files(config: Configuration):
    return [
        x
        for x in glob(f"{config.base_path}/{config.common}/**/*.yaml", recursive=True)
        if not re.match(f".*/{config.config_file_name}", x, re.I)
    ]


def _group_by_service_name(services_conf):
    return {
        k: list(v)
        for k, v in groupby(services_conf, operator.attrgetter("service_name"))
    }


def load_tool_config(
    base_path: str, config_file_name: str = "cloud-etc-config.yaml"
) -> Configuration:
    config_file_path = os.path.join(base_path, config_file_name)
    raw_config = _read_yaml_to_dict(config_file_path)
    logger.info("found config at: %s", config_file_path)
    config = Configuration(
        config_file_name=config_file_name,
        config_file_path=config_file_path,
        base_path=base_path,
        remote_base_key=raw_config["remote_base_key"],
        environment=raw_config["environment"],
        common=raw_config["common"],
        parameter_storage=raw_config["parameter_storage"],
    )
    logger.info("loaded config: %s", asdict(config))
    return config


def load_services_configurations(
    config: Configuration,
) -> Dict[str, ServiceConfiguration]:
    """
    scans all the configuration files and returns
    the service configurations for the target environment
    """
    services_conf = [
        ServiceConfiguration.from_raw_data(
            raw_configuration=_read_yaml_to_dict(f_path),
            path=f_path,
            environment=config.environment,
            remote_base_key=config.remote_base_key,
        )
        for f_path in _get_etc_files(config)
    ]

    services_common_conf = [
        ServiceConfiguration.from_raw_data(
            raw_configuration=_read_yaml_to_dict(f_path),
            path=f_path,
            environment="common",
            remote_base_key=config.remote_base_key,
        )
        for f_path in _get_etc_common_files(config)
    ]

    return _group_by_service_name(services_conf + services_common_conf)
