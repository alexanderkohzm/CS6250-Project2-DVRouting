#!/bin/bash

prefix="$1"
if [ -z "$prefix" ]; then
  echo "Usage: $0 <prefix>"
  exit 1
fi

for file in ${prefix}*.txt; do
  [ -e "$file" ] || continue
  name="${file%.txt}"
  echo "Running ./run.sh $name"
  ./run.sh "$name"
done
