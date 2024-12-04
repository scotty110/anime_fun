#!/bin/bash

eval "$(conda shell.bash hook)"                                           
conda activate frieren

uvicorn main:app --timeout-keep-alive 60 --port 9003 
