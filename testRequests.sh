#!/bin/sh

curl -vX POST localhost:8080 -d @sampleData.json \
--header "Content-Type: application/json"