from functools import reduce
from dataclasses import dataclass
import consul
import boto3
import botocore

from cloud_etc_configs.entities import Remotekey, ServiceConfiguration


class ConsulAdapter:
    def __init__(self, remote_base_key):
        self.client = consul.Consul()
        self.remote_base_key = remote_base_key

    def get_all_parameters(self):
        res = self.client.kv.get(self.remote_base_key, recurse=True)

        def to_remote_key(item):
            return Remotekey(key=item["Key"], value=item["Value"].decode())

        return [to_remote_key(x) for x in res[1]]

    def update_key(self, key, value):
        res = self.client.kv.put(key, value)
        return res

    def delete_key(self, key):
        res = self.client.kv.delete(key)
        return res

    def write_state(self, service_configuration: ServiceConfiguration):
        def encode_state(state):
            return "\n".join(state)

        response = self.client.kv.put(
            service_configuration.remote_state_path,
            encode_state(service_configuration.get_state()),
        )
        return response

    def get_current_state(self, service_configuration: ServiceConfiguration):
        def decode_state(state):
            return state.split("\n")

        response = self.client.kv.get(service_configuration.remote_state_path)
        item = response[1]
        if item:
            return Remotekey(
                key=item["Key"], value=decode_state(item["Value"].decode())
            )
        else:
            return Remotekey(key=service_configuration.remote_state_path, value="")
