#!/bin/bash
PORT="${APP_PORT:-8000}"

python3 api/manage.py migrate
python3 api/setup.py
python3 api/manage.py runserver 0.0.0.0:${PORT}