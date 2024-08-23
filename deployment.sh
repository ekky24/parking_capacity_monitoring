#!/bin/bash
NV="v2.6"
docker build -t parking_monitoring:$NV .

# # Tahu Sumedang
# docker stop parking_monitoring_tsu
# docker rm parking_monitoring_tsu
# docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="tsu" --name parking_monitoring_tsu --gpus all -d --restart unless-stopped parking_monitoring:$NV

# McD
docker stop parking_monitoring_mcd
docker rm parking_monitoring_mcd
docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="mcd" --name parking_monitoring_mcd --gpus all -d --restart unless-stopped parking_monitoring:$NV

# # SPKLU
# docker stop parking_monitoring_spklu
# docker rm parking_monitoring_spklu
# docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="spklu" --name parking_monitoring_spklu --gpus all -d --restart unless-stopped parking_monitoring:$NV

# # Ciganea 1
# docker stop parking_monitoring_cig_1
# docker rm parking_monitoring_cig_1
# docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="cig_1" --name parking_monitoring_cig_1 --gpus all -d --restart unless-stopped parking_monitoring:$NV

# # Ciganea 2
# docker stop parking_monitoring_cig_2
# docker rm parking_monitoring_cig_2
# docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="cig_2" --name parking_monitoring_cig_2 --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Solaria
docker stop parking_monitoring_sol
docker rm parking_monitoring_sol
docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="sol" --name parking_monitoring_sol --gpus all -d --restart unless-stopped parking_monitoring:$NV

# Starbucks
docker stop parking_monitoring_stb
docker rm parking_monitoring_stb
docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="stb" --name parking_monitoring_stb --gpus all -d --restart unless-stopped parking_monitoring:$NV

# # Masjid
# docker stop parking_monitoring_masjid
# docker rm parking_monitoring_masjid
# docker run --cpus="8" --ulimit nproc=8 --memory="2000m" --network="host" --log-opt max-size=10m --log-opt max-file=3 -e CCTV_AREA="masjid" --name parking_monitoring_masjid --gpus all -d --restart unless-stopped parking_monitoring:$NV