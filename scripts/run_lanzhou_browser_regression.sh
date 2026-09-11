#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${LAZYTRAVEL_BASE_URL:-https://lachlanchen.github.io/LazyTravel/china/cities/lanzhou/}"
RUNS="${1:-3}"
INVOCATION="$(date -u +%Y%m%dT%H%M%SZ)-$$"
ARTIFACT_ROOT="${LAZYTRAVEL_ARTIFACT_ROOT:-build/qa/playwright-regression/$INVOCATION}"

if ! [[ "$RUNS" =~ ^[1-9][0-9]*$ ]]; then
  echo "run count must be a positive integer" >&2
  exit 2
fi

for run in $(seq 1 "$RUNS"); do
  artifact_dir="$ARTIFACT_ROOT/run-${run}"
  mkdir -p "$artifact_dir"
  python -m pytest browser_tests/test_lanzhou_site.py \
    --base-url "$BASE_URL" \
    --browser-artifacts "$artifact_dir/failures" \
    --junitxml "$artifact_dir/junit.xml"
done
