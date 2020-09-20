from cloud_etc_configs.entities import ServiceConfiguration, Remotekey
from cloud_etc_configs.backends.etcd3 import Etcd3Adapter


def test_etc3_adapter():
    c = Etcd3Adapter("saul-test")
    c.update_key("saul-test/key_1", "val_1")
    c.update_key("saul-test/key_2", "val_2")
    c.update_key("saul-test/key_3", "val_3")

    res = c.get_all_parameters()
    print(res)

    res = c.delete_key("saul-test/key_2")
    print(res)

    service = ServiceConfiguration(
        environment="development",
        service_name="service_a",
        path="./environment/development/service_a.yaml",
        remote_state_path="saul-test/service_a/state-metadata",
        configurations=[
            Remotekey(key="saul-test/service_a/common_key_1", value="value_1"),
            Remotekey(key="saul-test/service_a/common_key_2", value="value_2_overrdie"),
            Remotekey(key="saul-test/service_a/key_1", value="updated"),
            Remotekey(key="saul-test/service_a/key_2", value="value_2"),
        ],
    )

    res = c.get_current_state(service)
    print(res)

    res = c.write_state(service)
    print(res)
