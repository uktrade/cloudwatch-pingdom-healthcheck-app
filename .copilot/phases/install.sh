#!/usr/bin/env bash

# Exit early if something goes wrong
set -e

yum install -y libxml2

pip install -r requirements.txt


# Add commands below to run as part of the install phase
