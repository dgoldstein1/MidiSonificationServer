#!/bin/sh

curl -vX POST localhost:8081 -d @sampleData.json \
--header "Content-Type: application/json"