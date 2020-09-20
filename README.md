# Cloud ETC Configs

A simple tool to sync configurations and secrets to configuration stores such as: ssm parameter store, consul, s3, vault, etcd, etc.

Problem Statement:

We need to be able to sync potentially hundreds of services configurations to multiple environments following a GitOps approach.
Current approaches like terraform create an syntax overhead for such a simple task, we wan to keep it simple here.
Researching current available options we couldn't find a generic one or that fit our needs, some were very specific, some very complex.

Sample usage:

```shell
cloud-etc-configs --path "environment/development" --dry-run
```

This will happen next:

1. cloud-etc-configs will scan the contents of the given path for yaml files
2. Loads the configuration given by `cloud-etc-config.yaml`
3. Combines the common configs with the target configs
4. Compute a diff between the local and remote state
5. Applies if no dry-run the differences to the remote store

This tool can be combined with a CI/CD flow or a web-server listening to GitHub hooks and automatically sync.

## To Do

- support for secrets and sops
- add s3 remote store
- add CD examples
- add unit tests
- package as pip
- implement additional function to add secrets e.g. to mount it in a webserver or job

## Additional Notes

The tool will store some metadata in the remote store, this metadata is used to detect deletions.

To read from ssm and inject to the application environment there are some options to pick:

- https://github.com/remind101/ssm-env
- https://github.com/gmr/env-aws-params
