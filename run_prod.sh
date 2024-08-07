#!/bin/bash

DOCKER_COMPOSE_FILE="docker-compose.prod.yml"

if [ ! -f "$DOCKER_COMPOSE_FILE" ]; then
    echo "Error: Docker Compose file '$DOCKER_COMPOSE_FILE' not found."
    exit 1
fi

ENV_FILE=".prod"

if [ -f "$ENV_FILE" ]; then
    echo "Loading environment variables from $ENV_FILE"
    export $(grep -v '^#' $ENV_FILE | xargs)
else
    echo "Error: .prod file '$ENV_FILE' for Docker Compose not found."
    exit 1
fi

docker-compose -f "$DOCKER_COMPOSE_FILE" up -d