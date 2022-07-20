#!/usr/bin/env bash

# install RTL-SDR and Python 3
sudo apt install rtl-sdr -y
sudo apt install python3-venv python3-pip pylint -y

# install python pipenv
pip3 install pipenv --user

# Have to call pipenv directly since it is not yet on the user PATH
PIPENV="${HOME}/.local/bin/pipenv"

# Install the python virtual environment
${PIPENV} install

# Get the location of the virtual environment.
# Have to use tail to work around a bug, here:
# https://github.com/pypa/setuptools/issues/3278
LOCATION="$( ${PIPENV} --where | tail -1)"



# TODO: export the env vars then paste them into /etc/environment.d/adsb.conf
# I had been installing Kafka locally but I would rather install it on
# another server. Then the ADSB_KAFKA_CONFIG could be input through this script
# and not managed locally

# Create environment variables
# export ADSB_KAFKA_CONFIG=
# export ADSB_KAFKA_TOPIC=adsb
# export ADSB_PYTHON_PATH="${LOCATION}"
