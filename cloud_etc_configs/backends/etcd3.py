from functools import reduce
from dataclasses import dataclass
import etcd3

from cloud_etc_configs.entities import Remotekey, ServiceConfiguration


class Etcd3Adapter:
    def __init__(self, remote_base_key):
        self.client = etcd3.client(host="localhost", port=9500)
        self.remote_base_key = remote_base_key

    def get_all_parameters(self):
        res = self.client.get_prefix(self.remote_base_key)

        def to_remote_key(item):
            return Remotekey(key=item[1].key.decode(), value=item[0].decode())

        return [to_remote_key(x) for x in res]

    def update_key(self, key, value):
        res = self.client.put(key, value)
        return res

    def delete_key(self, key):
        res = self.client.delete(key)
        return res

    def write_state(self, service_configuration: ServiceConfiguration):
        def encode_state(state):
            return "\n".join(state)

        response = self.client.put(
            service_configuration.remote_state_path,
            encode_state(service_configuration.get_state()),
        )
        return response

    def get_current_state(self, service_configuration: ServiceConfiguration):
        def decode_state(state):
            return state.split("\n")

        response = self.client.get(service_configuration.remote_state_path)
        if response[0]:
            return Remotekey(
                key=response[1].key.decode(), value=decode_state(response[0].decode())
            )
        else:
            return Remotekey(key=service_configuration.remote_state_path, value="")
