#!/bin/bash
set -eu

GO_HTTP=https://go.dev/dl/go1.23.4.linux-amd64.tar.gz

curl -L $GO_HTTP -o go.tar.gz && sudo tar -xf go.tar.gz -C /usr/local && rm go.tar.gz

cat >> $HOME/.crc << EOF

export GO_HOME="/usr/local/go"
export PATH="\$GO_HOME/bin:\$PATH"
EOF