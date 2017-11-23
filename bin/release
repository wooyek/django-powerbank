#!/usr/bin/env bash

echo "AUTO_MIGRATE: $AUTO_MIGRATE"

if [[ "$AUTO_MIGRATE" == "True" ]]; then
    echo "=> Performing database migrations"
    python example_project/manage.py migrate --noinput
fi
