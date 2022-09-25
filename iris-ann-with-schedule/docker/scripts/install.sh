#!/bin/bash

# Bash "strict mode", to help catch problems and bugs in the shell
# script. Every bash script you write should include this. See
# http://redsymbol.net/articles/unofficial-bash-strict-mode/ for
# details.
set -euo pipefail

# Tell apt-get we're never going to be able to give manual
# feedback:
export DEBIAN_FRONTEND=noninteractive

# Update lists
apt-get update

# Security updates
apt-get -y upgrade

# Install needed libraries
apt-get install -y --no-install-recommends python3-dev g++

# Delete cached files we don't need anymore:
apt-get clean
rm -rf /var/lib/apt/lists/*
