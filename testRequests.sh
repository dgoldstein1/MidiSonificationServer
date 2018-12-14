#!/bin/sh

curl -vX POST localhost:3028 -d @sampleData.json \
--header "Content-Type: application/json"