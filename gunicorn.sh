#!/bin/sh
gunicorn yolo_app_park_web:app -c gunicorn_config.py