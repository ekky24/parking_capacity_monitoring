#!/bin/sh
PYTHONPATH=dist gunicorn dist.yolo_app_park_web:app -c gunicorn_config.py