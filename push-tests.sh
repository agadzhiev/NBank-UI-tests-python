#!/bin/bash

IMAGE_NAME="nbank-tests"
DOCKER_USERNAME="agadzhiev"
TAG="latest"

if [ -z "$DOCKERHUB_TOKEN" ]; then
    echo "Error: DOCKERHUB_TOKEN is not set"
    exit 1
fi

echo "$DOCKERHUB_TOKEN" | docker login --username "$DOCKER_USERNAME" --password-stdin

docker tag "$IMAGE_NAME" "$DOCKER_USERNAME/$IMAGE_NAME:$TAG"

docker push "$DOCKER_USERNAME/$IMAGE_NAME:$TAG"

echo "Image pushed. To pull it run:"
echo "docker pull $DOCKER_USERNAME/$IMAGE_NAME:$TAG"
