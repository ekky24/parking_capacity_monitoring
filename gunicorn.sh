#!/bin/sh
PYTHONUNBUFFERED=TRUE PYTHONPATH=dist gunicorn dist.yolo_app_park_web_2:app -c gunicorn_config.py