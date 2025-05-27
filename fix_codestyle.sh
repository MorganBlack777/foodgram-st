#!/bin/bash

if [ -f "$(which black)" ]; then
  black backend/ --config pyproject.toml
else
 # Not exists
 pip3 install black
 black backend/ --config pyproject.toml
fi

ruff check

flake8 | grep W
flake8 | grep E
