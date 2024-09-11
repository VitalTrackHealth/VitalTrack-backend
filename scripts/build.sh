#!/bin/bash

# Install PDM
curl -sSL https://pdm-project.org/install-pdm.py | python3 -

# Install dependencies using PDM
pdm install
