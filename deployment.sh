#!/bin/bash
NV="v1.0"
docker build -t parking_monitoring:$NV .

# Tahu Sumedang
docker rm parking_monitoring_tsu
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="tsu" --name parking_monitoring_tsu -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# McD
docker rm parking_monitoring_mcd
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="mcd" --name parking_monitoring_mcd -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# SPKLU
docker rm parking_monitoring_spklu
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="spklu" --name parking_monitoring_spklu -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Ciganea
docker rm parking_monitoring_cig
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="cig" --name parking_monitoring_cig -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Solaria
docker rm parking_monitoring_sol
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring_sol -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Starbucks
docker rm parking_monitoring_stb
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="stb" --name parking_monitoring_stb -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Masjid
docker rm parking_monitoring_masjid
docker run --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="masjid" --name parking_monitoring_masjid -v /mnt/data/machine_learning/output:/app/output --gpus all -d --restart unless-stopped parking_monitoring:$NV