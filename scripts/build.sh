#!/bin/bash

# Install PDM
curl -sSL https://pdm-project.org/install-pdm.py | python3 -
export PATH=/home/.local/bin:$PATH

# Install dependencies using PDM
pdm install
