#!/bin/bash

set -e

echo "Installing backend dependencies..."

cd /opt/app

/opt/app/venv/bin/pip install --upgrade pip

/opt/app/venv/bin/pip install -r /opt/app/requirements.txt

chown -R appuser:appuser /opt/app

echo "Dependencies installed successfully."