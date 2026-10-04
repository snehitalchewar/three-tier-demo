#!/bin/bash
set -e

sleep 5

systemctl is-active --quiet three-tier-backend.service

curl --fail http://localhost:8000/api/health