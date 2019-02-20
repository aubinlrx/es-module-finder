#!/bin/bash

PACKAGE_PATH="$HOME/.config/sublime-text-3/Packages/EsModuleFinder"

if [ ! -d "$PACKAGE_PATH" ]; then
  mkdir -p "$PACKAGE_PATH";
fi

ln -s "./Main.sublime-menu" "$PACKAGE_PATH/Main.sublime-menu"
ln -s "./EsModuleFinder.sublime-settings" "$PACKAGE_PATH/EsModuleFinder.sublime-settings"
ln -s "./EsModuleFinder.py" "$PACKAGE_PATH/EsModuleFinder.py"
ln -s "./Default (Linux).sublime-keymap" "$PACKAGE_PATH/Default (Linux).sublime-keymap"
ln -s "./Default (OSX).sublime-keymap" "$PACKAGE_PATH/Default (OSX).sublime-keymap"
ln -s "./Default (Windows).sublime-keymap" "$PACKAGE_PATH/Default (Windows).sublime-keymap"
