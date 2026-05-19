#!/usr/bin/env bash
set -euo pipefail

COVERAGE_FILE="${1:-swagger-coverage-report/coverage.json}"
THRESHOLD="${2:-50}"

if [ ! -f "$COVERAGE_FILE" ]; then
  echo "ERROR: coverage file not found: $COVERAGE_FILE"
  exit 1
fi

TOTAL=$(jq '.total' "$COVERAGE_FILE")
COVERED=$(jq '.covered' "$COVERAGE_FILE")
PERCENTAGE=$(jq '.percentage' "$COVERAGE_FILE")

echo "===== API Coverage Quality Gate ====="
echo "Endpoints total:   $TOTAL"
echo "Endpoints covered: $COVERED"
echo "Coverage:          ${PERCENTAGE}%"
echo "Threshold:         ${THRESHOLD}%"
echo "======================================"

if (( $(echo "$PERCENTAGE < $THRESHOLD" | bc -l) )); then
  echo "FAILED: API coverage ${PERCENTAGE}% is below ${THRESHOLD}% threshold"
  exit 1
fi

echo "PASSED: API coverage meets the threshold"
