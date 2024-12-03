#!/bin/bash

mkdir ./bin
export GOBIN=$PWD/bin
export PATH=$GOBIN:$PATH                                                        

go install github.com/twitchtv/twirp/protoc-gen-twirp@latest
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install github.com/verloop/twirpy/protoc-gen-twirpy@latest
