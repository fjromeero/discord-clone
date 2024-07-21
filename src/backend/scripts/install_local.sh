#!/bin/bash

echoNeedInstall()
{
    echo "########################################################################"
    echo " Installing $1"
    echo "########################################################################"
}

# Tools and dependencies
if ! wich pip3 >/dev/null; then
    echoNeedInstall pip3
    sudo apt-get install python3-pip
fi

if ! wich virtualenv >/dev/null; then
    echoNeedInstall virtualenv
    sudo apt-get install python3-virtualenv
fi

# Clean, create and activate the virtual env
sudo rm -R venv
virtualenv --python=/usr/bin/python3.10 --system-site-packages venv
. venv/bin/activate

# Install dependencies
pip install -r requirements.txt --upgrade --force-reinstall

# Deactivate virtual env
deactivate