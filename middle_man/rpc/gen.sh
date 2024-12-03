#!/bin/bash
protoc --go_out=. --twirp_out=. *.proto
