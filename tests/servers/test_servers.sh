#!/bin/bash

export ETCD_ADDR=http://127.0.0.1:9500
export CONSUL_ADDR=http://127.0.0.1:8500

curl \
    -L \
    -X PUT \
    --data @tests/servers/contents \
    $CONSUL_ADDR/v1/kv/my-key

curl -L "$ETCD_ADDR/version"
echo ""

curl -L -X POST $ETCD_ADDR/v3/kv/range -d '{"key": "Zm9v", "value": "YmFy"}'
