#!/bin/bash

set -m
npm start --prefix /usr/src/app/FUXA/server &

while ! curl http://localhost:1881 > /dev/null
do
  echo "$(date) - still trying"
  sleep 1
done
echo "$(date) - connected successfully"
echo "uploading config"
curl -X POST -H "Content-Type: application/json" --data-binary "@../config/fuxa-project.json" http://localhost:1881/api/project

fg %1