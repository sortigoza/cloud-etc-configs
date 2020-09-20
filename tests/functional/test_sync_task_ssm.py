import os
from cloud_etc_configs.sync_task import SyncTask
from cloud_etc_configs.logger import get_logger
from cloud_etc_configs.adapters import get_remote_handler

logger = get_logger()
logger.setLevel("DEBUG")
task = SyncTask()

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "../fixtures")
base_path = os.path.join(FIXTURES_DIR, "sync_task_ssm/development")

# NOTE: for these tests to work valid AWS credentials are expected in the environment
def test_exeute_for_ssm():
    task.execute(base_path=base_path)
    remote_handler = get_remote_handler(
        task.config.parameter_storage, task.config.remote_base_key
    )

    all_parameters = set(
        f"{x.key}={x.value}" for x in remote_handler.get_all_parameters()
    )
    expected = set(
        [
            "/saul-test/service_a/common_key_1=value_1",
            "/saul-test/service_a/state-metadata=/saul-test/service_a/common_key_1\n/saul-test/service_a/common_key_2\n/saul-test/service_a/key_1\n/saul-test/service_a/key_2",
            "/saul-test/service_a/key_2=value_2",
            "/saul-test/service_a/common_key_2=value_2_overrdie",
            "/saul-test/service_b/key_2=value_2",
            "/saul-test/service_b/key_1=value_1",
            "/saul-test/service_a/key_1=value_1",
            "/saul-test/service_b/state-metadata=/saul-test/service_b/key_1\n/saul-test/service_b/key_2\n/saul-test/service_b/key_3\n/saul-test/service_b/key_4",
            "/saul-test/service_b/key_4=value_4",
            "/saul-test/test=test",
            "/saul-test/service_b/key_3=value_3",
        ]
    )

    # all excpected parameters are present
    assert expected - all_parameters == set()
