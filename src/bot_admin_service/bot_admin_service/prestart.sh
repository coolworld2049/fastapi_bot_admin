#! /usr/bin/env bash

python ./bot_admin_service/pre_start.py

# alembic upgrade head

python ./bot_admin_service/initial_data.py

#pytest ./bot_admin_service/test -vv --tb=native -l --cov ./bot_admin_service --cov-report=html
