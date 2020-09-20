from cloud_etc_configs.entities import ServiceConfiguration, Remotekey
from cloud_etc_configs.sync_task import SyncTask


def test_combine_with_common_configurations():
    task = SyncTask()
    grouped_by_service_name = {
        "service_a": [
            ServiceConfiguration(
                environment="development",
                service_name="service_a",
                path=f"sample-path/service_a.yaml",
                remote_state_path="/test/service_a/state-metadata",
                configurations=[
                    Remotekey(key="/test/service_a/key_1", value="value_1"),
                    Remotekey(key="/test/service_a/key_2", value="value_2"),
                    Remotekey(
                        key="/test/service_a/common_key_2", value="value_2_overrdie"
                    ),
                ],
            ),
            ServiceConfiguration(
                environment="common",
                service_name="service_a",
                path=f"sample-path/../common/service_a.yaml",
                remote_state_path="/test/service_a/state-metadata",
                configurations=[
                    Remotekey(key="/test/service_a/common_key_1", value="value_1"),
                    Remotekey(key="/test/service_a/common_key_2", value="value_2"),
                ],
            ),
        ]
    }

    combined = task.combine_with_common_configurations(grouped_by_service_name)
    expected = [
        ServiceConfiguration(
            environment="development",
            service_name="service_a",
            path="sample-path/service_a.yaml",
            remote_state_path="/test/service_a/state-metadata",
            configurations=[
                Remotekey(key="/test/service_a/common_key_1", value="value_1"),
                Remotekey(key="/test/service_a/common_key_2", value="value_2_overrdie"),
                Remotekey(key="/test/service_a/key_1", value="value_1"),
                Remotekey(key="/test/service_a/key_2", value="value_2"),
            ],
        )
    ]
    assert combined == expected
