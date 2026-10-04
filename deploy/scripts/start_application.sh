#!/bin/bash

set -e

echo "Starting three-tier backend..."

chown -R appuser:appuser /opt/app

systemctl daemon-reload

systemctl enable three-tier-backend.service

systemctl restart three-tier-backend.service

sleep 5

systemctl is-active --quiet three-tier-backend.service

echo "Backend started successfully."