#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd workflow_engine

python manage.py collectstatic --no-input
python manage.py migrate