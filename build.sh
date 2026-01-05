#!/bin/bash
set -e
cd "$(dirname "$0")"

docker build -t team-pypartners .
docker tag team-pypartners fdewpi/team-pypartners
docker push fdewpi/team-pypartners