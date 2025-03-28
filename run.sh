#!/bin/bash

if [ "$ENVIRONMENT" == "production" ]; then
    # Cloud environment - use PORT from environment
    gunicorn --bind :$PORT app:app
else
    # Local environment - use port 8080
    gunicorn --config gunicorn_config.py app:app
fi