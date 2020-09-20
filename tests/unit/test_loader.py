import os

import pytest

from cloud_etc_configs.entities import Remotekey, ServiceConfiguration
from cloud_etc_configs.loader import load_services_configurations, load_tool_config

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "../fixtures")


def test_load_tool_config():
    base_path = os.path.join(FIXTURES_DIR, "loader/defaults")
    config_file = "cloud-etc-config.yaml"
    config = load_tool_config(base_path)
    assert config.config_file_name == config_file
    assert config.config_file_path == os.path.join(base_path, config_file)
    assert config.base_path == base_path
    assert config.remote_base_key == "/test"
    assert config.environment == "development"
    assert config.common == "../common"
    assert config.parameter_storage == "ssm"


def test_load_tool_config_with_non_default():
    base_path = os.path.join(FIXTURES_DIR, "loader/non-defaults")
    config_file = "non-default-config.yaml"
    config = load_tool_config(base_path, config_file_name=config_file)
    assert config.config_file_name == config_file
    assert config.config_file_path == os.path.join(base_path, config_file)
    assert config.base_path == base_path
    assert config.remote_base_key == "/test"
    assert config.environment == "development"
    assert config.common == "../common"
    assert config.parameter_storage == "ssm"


def test_load_tool_config_with_non_existent():
    base_path = os.path.join(FIXTURES_DIR, "loader/non-existent")
    with pytest.raises(FileNotFoundError):
        load_tool_config(base_path)


def test_load_services_configurations():
    base_path = os.path.join(FIXTURES_DIR, "loader/defaults")
    config = load_tool_config(base_path)
    services = load_services_configurations(config)
    service_a = services["service_a"]
    service_b = services["service_b"]
    # there is a common + the env service
    assert len(service_a) == 2
    # only the env service
    assert len(service_b) == 1

    expected_service_a = [
        ServiceConfiguration(
            environment="development",
            service_name="service_a",
            path=f"{FIXTURES_DIR}/loader/defaults/service_a.yaml",
            remote_state_path="/test/service_a/state-metadata",
            configurations=[
                Remotekey(key="/test/service_a/key_1", value="value_1"),
                Remotekey(key="/test/service_a/key_2", value="value_2"),
                Remotekey(key="/test/service_a/common_key_2", value="value_2_overrdie"),
            ],
        ),
        ServiceConfiguration(
            environment="common",
            service_name="service_a",
            path=f"{FIXTURES_DIR}/loader/defaults/../common/service_a.yaml",
            remote_state_path="/test/service_a/state-metadata",
            configurations=[
                Remotekey(key="/test/service_a/common_key_1", value="value_1"),
                Remotekey(key="/test/service_a/common_key_2", value="value_2"),
            ],
        ),
    ]
    assert service_a == expected_service_a

    expected_service_b = [
        ServiceConfiguration(
            environment="development",
            service_name="service_b",
            path=f"{FIXTURES_DIR}/loader/defaults/service_b.yaml",
            remote_state_path="/test/service_b/state-metadata",
            configurations=[
                Remotekey(key="/test/service_b/key_1", value="value_1"),
                Remotekey(key="/test/service_b/key_2", value="value_2"),
                Remotekey(key="/test/service_b/key_3", value="value_3"),
                Remotekey(key="/test/service_b/key_4", value="value_4"),
            ],
        )
    ]
    assert service_b == expected_service_b
