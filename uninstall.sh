#!/bin/bash

DIRECTORY_PATH="$HOME/.config/sublime-text-3/Packages/EsModuleFinder"

if [ -d "$DIRECTORY_PATH" ]; then
  rm -rf "$DIRECTORY_PATH"
fi
