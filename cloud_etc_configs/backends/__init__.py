import boto3
from cloud_etc_configs.backends.ssm_parameter_store import SSMAdapter
from cloud_etc_configs.backends.etcd3 import Etcd3Adapter


def get_remote_handler(name, remote_base_key):
    if name == "ssm":
        aws_session = boto3.session.Session()
        return SSMAdapter(aws_session, remote_base_key)
    elif name == "etcd3":
        return Etcd3Adapter(remote_base_key)
    elif name == "consul":
        return Etcd3Adapter(remote_base_key)
    raise Exception(f"{name} did not match any of the available options")
