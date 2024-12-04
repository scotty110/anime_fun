#!/bin/bash
protoc -I ../middle_man/rpc/ --python_out=./ --twirpy_out=./ ../middle_man/rpc/llm.proto