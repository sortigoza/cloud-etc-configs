from cloud_etc_configs.entities import PlanDiff, ServiceConfiguration


class TestServiceConfiguration:
    @staticmethod
    def test_from_raw_data():
        service_name = "test-name"
        raw_configuration = {
            "service_name": service_name,
            "configuration": {"key_1": "val_1", "key_2": "val_2"},
        }
        path = "./test-path"
        environment = "test-env"
        remote_base_key = "/base-key"
        res = ServiceConfiguration.from_raw_data(
            raw_configuration, path, environment, remote_base_key
        )
        assert res.environment == environment
        assert res.service_name == service_name
        assert res.path == path
        assert (
            res.remote_state_path == f"{remote_base_key}/{service_name}/state-metadata"
        )
        first_key = res.configurations[0]
        assert first_key.key == f"{remote_base_key}/{service_name}/key_1"
        assert first_key.value == "val_1"

    @staticmethod
    def test_add_common_keys():
        service_name = "test-name"
        raw_configuration = {
            "service_name": service_name,
            "configuration": {
                "key_1": "overwrite",
            },
        }
        raw_configuration_common = {
            "service_name": service_name,
            "configuration": {"key_1": "val_1", "key_2": "val_2"},
        }
        path = "./test-path"
        environment = "test-env"
        remote_base_key = "/base-key"
        env = ServiceConfiguration.from_raw_data(
            raw_configuration, path, environment, remote_base_key
        )
        common = ServiceConfiguration.from_raw_data(
            raw_configuration_common, path, "common", remote_base_key
        )
        res = env.add_common_keys(common)
        configurations = {x.key: x.value for x in res.configurations}
        # present in common but overwritten
        key_1_key = f"{remote_base_key}/{service_name}/key_1"
        assert key_1_key in configurations
        assert configurations[key_1_key] == "overwrite"
        # present only in common
        assert f"{remote_base_key}/{service_name}/key_2" in configurations

    @staticmethod
    def test_add_common_keys_w_empty():
        service_name = "test-name"
        raw_configuration = {
            "service_name": service_name,
            "configuration": {
                "key_1": "val_1",
            },
        }
        path = "./test-path"
        environment = "test-env"
        remote_base_key = "/base-key"
        env = ServiceConfiguration.from_raw_data(
            raw_configuration, path, environment, remote_base_key
        )
        common = None
        res = env.add_common_keys(common)
        configurations = {x.key: x.value for x in res.configurations}
        # present in common but overwritten
        key_1_key = f"{remote_base_key}/{service_name}/key_1"
        assert key_1_key in configurations
        assert configurations[key_1_key] == "val_1"

    @staticmethod
    def test_get_state():
        service_name = "test-name"
        raw_configuration = {
            "service_name": service_name,
            "configuration": {"key_1": "val_1", "key_2": "val_2"},
        }
        path = "./test-path"
        environment = "test-env"
        remote_base_key = "/base-key"
        res = ServiceConfiguration.from_raw_data(
            raw_configuration, path, environment, remote_base_key
        ).get_state()
        assert res == ["/base-key/test-name/key_1", "/base-key/test-name/key_2"]


class TestPlanDiff:
    @staticmethod
    def test_mutable_defaults():
        obj = PlanDiff.new_with_mutable_defaults()
        assert obj.ok == []
        obj.ok.append("hi")
        assert obj.ok == ["hi"]
