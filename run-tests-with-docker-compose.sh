#!/usr/bin/env bash

IMAGE_NAME="${IMAGE_NAME:-nbank-tests}"
APIBASEURL="${APIBASEURL:-http://localhost:4111}"
UIBASEURL="${UIBASEURL:-http://localhost:3000}"

echo "Starting test environment with docker compose..."
docker compose up -d

echo "Running tests container..."
docker run --rm \
  -e APIBASEURL="${APIBASEURL}" \
  -e UIBASEURL="${UIBASEURL}" \
  -e server="${APIBASEURL}" \
  -e UI_BASE_URL="${UIBASEURL}" \
  "${IMAGE_NAME}"
TEST_EXIT_CODE=$?

echo "Stopping test environment..."
docker compose down

exit "${TEST_EXIT_CODE}"
