#!/usr/bin/env bash

echo "AUTO_MIGRATE: $AUTO_MIGRATE"

if [[ "$AUTO_MIGRATE" == "True" ]]; then
    echo "=> Performing database migrations"
    python example_project/manage.py migrate --noinput
    python example_project/manage.py opt_out_feedback_defaults --on-empty
fi
