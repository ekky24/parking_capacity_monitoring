#!/bin/bash
NV="trial"
docker build -f Dockerfile_trial -t parking_monitoring:$NV .

# Solaria
# docker stop parking_monitoring_trial_sol
# docker rm parking_monitoring_trial_sol
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring_trial_sol -v /mnt/nvme2n1/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV