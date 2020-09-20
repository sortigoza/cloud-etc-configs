from cloud_etc_configs.entities import Remotekey, ServiceConfiguration


class SSMAdapter:
    def __init__(self, aws_session, remote_base_key):
        self.aws_session = aws_session
        self.client = self.aws_session.client("ssm")
        self.remote_base_key = remote_base_key

    def get_all_parameters(self):
        parameters = self._get_parameters()
        return [self._get_parameter(x["Name"]) for x in parameters]

    def update_key(self, key, value):
        print(f"updating key {key} = {value}")
        response = self.client.put_parameter(
            Name=key,
            Description="managed by cloud-etc-config",
            Value=value,
            Overwrite=True,
            Type="String",
        )

        return response

    def delete_key(self, key):
        response = self.client.delete_parameter(
            Name=key,
        )

        return response

    def write_state(self, service_configuration: ServiceConfiguration):
        def encode_state(state):
            return "\n".join(state)

        response = self.client.put_parameter(
            Name=service_configuration.remote_state_path,
            Description="managed by cloud-etc-config (state metadata)",
            Value=encode_state(service_configuration.get_state()),
            Overwrite=True,
            Type="String",
        )

        return response

    def get_current_state(self, service_configuration: ServiceConfiguration):
        def decode_state(state):
            return state.split("\n")

        response = self._get_parameter(service_configuration.remote_state_path)

        return decode_state(response.value)

    def _get_parameters(self):
        result = self.client.describe_parameters(
            ParameterFilters=[
                {
                    "Key": "Name",
                    "Option": "BeginsWith",
                    "Values": [
                        self.remote_base_key,
                    ],
                },
            ],
        )
        next_token = result.get("NextToken")
        parameters = result["Parameters"]

        while next_token:
            result = self.client.describe_parameters(
                ParameterFilters=[
                    {
                        "Key": "Name",
                        "Option": "BeginsWith",
                        "Values": [
                            self.remote_base_key,
                        ],
                    },
                ],
                NextToken=next_token,
            )
            next_token = result.get("NextToken")
            parameters += result["Parameters"]
        return parameters

    def _get_parameter(self, name):
        try:
            response = self.client.get_parameter(
                Name=name,
            )["Parameter"]
            return Remotekey(key=response["Name"], value=response["Value"])
        except self.client.exceptions.ParameterNotFound:
            return Remotekey(key=name, value="")
