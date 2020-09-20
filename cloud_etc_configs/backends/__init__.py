import boto3
from cloud_etc_configs.backends.ssm_parameter_store import SSMAdapter


def get_remote_handler(name, remote_base_key):
    if name == "ssm":
        aws_session = boto3.session.Session()
        return SSMAdapter(aws_session, remote_base_key)
    raise Exception(f"{name} did not match any of the available options")
