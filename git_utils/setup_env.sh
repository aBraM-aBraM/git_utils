#!/usr/bin/env sh

PROJECT_DIR=$(dirname "$( cd -- "$(dirname "$0")" >/dev/null 2>&1 || exit ; pwd -P )")
HOOKS_DIR="$PROJECT_DIR"/.git/hooks
echo "$PROJECT_DIR"

for file in "$(dirname "$0")"/hooks/*
do
  echo "cp $file $HOOKS_DIR"
  cp "$file" "$HOOKS_DIR"
  echo "chmod +x $HOOKS_DIR/$(basename "$file")"
  chmod +x "$HOOKS_DIR/$(basename "$file")"
done