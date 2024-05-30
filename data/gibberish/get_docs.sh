#!/bin/bash

# early work to run scripts against the local ollama instance

HOST=localhost
PORT=11434
STREAM=false
MODEL="mistral:latest"
PROMPT="$2"
DOMAIN="$1"
BASEDIR=$(dirname $0)

DATA='{"model": "mistral:latest", "prompt": "'"$PROMPT?"'", "stream": false}'

RESPONSE=$(curl \
  -X POST \
  --header "Content-Type: application/json" \
  "$HOST:$PORT/api/generate" \
  -q -s \
  --data "$DATA" | jq -r ".response")

echo "$RESPONSE" > "$BASEDIR"/output/"$DOMAIN".md
