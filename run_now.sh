#!/bin/bash

docker build --no-cache -t enbw-api .

docker run --name enbw-api -p 8000:8000 enbw-api
