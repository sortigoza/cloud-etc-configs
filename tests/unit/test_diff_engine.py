from cloud_etc_configs.diff_engine import compute_diff
from cloud_etc_configs.entities import PlanDiff, Remotekey, ServiceConfiguration

all_existing_parameters = [
    Remotekey(key="/saul-test/service_a/common_key_1", value="value_1"),
    Remotekey(key="/saul-test/service_a/common_key_2", value="value_2_overrdie"),
    Remotekey(key="/saul-test/service_a/key_1", value="value_1"),
    Remotekey(key="/saul-test/service_a/key_2", value="value_2"),
    Remotekey(key="/saul-test/service_b/key_1", value="value_1"),
    Remotekey(key="/saul-test/service_b/key_3", value="value_3"),
    Remotekey(key="/saul-test/service_b/key_4", value="value_4"),
    Remotekey(key="/saul-test/test", value="test"),
    # Remotekey(key="/saul-test/service_b/key_2", value="value_2"), # to be created
]

current_states = {
    "service_a": [
        "/saul-test/service_a/common_key_1",
        "/saul-test/service_a/common_key_2",
        "/saul-test/service_a/key_1",
        "/saul-test/service_a/key_2",
    ],
    "service_b": [
        "/saul-test/service_b/key_1",
        # "/saul-test/service_b/key_2", # to be created
        "/saul-test/service_b/key_3",
        "/saul-test/service_b/key_4",
    ],
}


env_services_configurations = [
    ServiceConfiguration(
        environment="development",
        service_name="service_b",
        path="./environment/development/service_b.yaml",
        remote_state_path="/saul-test/service_b/state-metadata",
        configurations=[
            Remotekey(key="/saul-test/service_b/key_1", value="value_1"),
            Remotekey(key="/saul-test/service_b/key_2", value="value_2"),
            # Remotekey(key="/saul-test/service_b/key_3", value="value_3"), # to be deleted
            Remotekey(key="/saul-test/service_b/key_4", value="value_4"),
        ],
    ),
    ServiceConfiguration(
        environment="development",
        service_name="service_a",
        path="./environment/development/service_a.yaml",
        remote_state_path="/saul-test/service_a/state-metadata",
        configurations=[
            Remotekey(key="/saul-test/service_a/common_key_1", value="value_1"),
            Remotekey(
                key="/saul-test/service_a/common_key_2", value="value_2_overrdie"
            ),
            Remotekey(
                key="/saul-test/service_a/key_1", value="updated"
            ),  # to be updated
            Remotekey(key="/saul-test/service_a/key_2", value="value_2"),
        ],
    ),
]


def test_compute_diff_all_actions():
    diff = compute_diff(
        current_states, all_existing_parameters, env_services_configurations
    )
    expected_diff_0 = PlanDiff(
        ok=[
            Remotekey(key="/saul-test/service_b/key_1", value="value_1"),
            Remotekey(key="/saul-test/service_b/key_4", value="value_4"),
        ],
        create=[Remotekey(key="/saul-test/service_b/key_2", value="value_2")],
        update=[],
        delete=[Remotekey(key="/saul-test/service_b/key_3", value="")],
    )
    assert diff[0]["diff"] == expected_diff_0
    expected_diff_1 = PlanDiff(
        ok=[
            Remotekey(key="/saul-test/service_a/common_key_1", value="value_1"),
            Remotekey(
                key="/saul-test/service_a/common_key_2", value="value_2_overrdie"
            ),
            Remotekey(key="/saul-test/service_a/key_2", value="value_2"),
        ],
        create=[],
        update=[Remotekey(key="/saul-test/service_a/key_1", value="updated")],
        delete=[],
    )
    assert diff[1]["diff"] == expected_diff_1
