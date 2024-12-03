#!/bin/bash
# Tell go to look inside $PWD/bin
# Im not sure how this all works under the hood

#mkdir ./bin
export GOBIN=$PWD/bin
export PATH=$GOBIN:$PATH
