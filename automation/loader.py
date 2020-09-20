from itertools import groupby
import operator
from glob import glob
import yaml

from automation.entities import ServiceConfiguration, Configuration


def _read_yaml_to_dict(file_path) -> dict:
    with open(file_path, "r") as f:
        return yaml.safe_load(f.read())


def _get_etc_files():
    return list(glob("environment/**/*.yaml"))


def _group_by_service_name(services_conf):
    return {
        k: list(v)
        for k, v in groupby(services_conf, operator.attrgetter("service_name"))
    }


def load_configurations(config: Configuration):
    """
    scans all the configuration files and returns
    the service configurations for the target environment
    """
    files = _get_etc_files()

    services_conf = []
    for f_path in files:
        service_config = ServiceConfiguration.from_path_and_data(
            path=f_path,
            raw_configuration=_read_yaml_to_dict(f_path),
            remote_base_path=config.base_path,
        )
        if service_config.environment in (config.target_environment, "common"):
            services_conf.append(service_config)

    return _group_by_service_name(services_conf)
