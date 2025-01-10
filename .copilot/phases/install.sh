#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

apt-get update && apt-get install -y libxml2

pip install requirements.txt


# Add commands below to run as part of the install phase
