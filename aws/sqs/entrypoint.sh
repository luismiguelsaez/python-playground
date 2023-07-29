#!/usr/bin/env bash

set -e

if [ $# -eq 0 ]; then
  echo "No arguments provided!!"
  exit 1
else
  if [ "$1" = "consumer" ]; then
    exec python3 /app/sqs.py
  elif [ "$1" = "producer" ]; then
    exec python3 /app/sns.py
  else
    echo "Invalid argument!!"
    exit 1
  fi
fi
