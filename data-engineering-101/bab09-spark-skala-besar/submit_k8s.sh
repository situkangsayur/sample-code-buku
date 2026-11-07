#!/usr/bin/env bash
# Kode 9.9: mengirim job ke Kubernetes dengan event log dan dynamic allocation.
# Sesuaikan alamat API server, image, dan kredensial S3 dengan klaster Anda.
set -euo pipefail
API=${API:-https://api.klaster.internal:6443}
IMAGE=${IMAGE:-registry.internal/spark-bank:1.0}

spark-submit \
  --master "k8s://${API}" \
  --deploy-mode cluster \
  --name gold-harian \
  --conf spark.kubernetes.namespace=data \
  --conf spark.kubernetes.authenticate.driver.serviceAccountName=spark \
  --conf spark.kubernetes.container.image="${IMAGE}" \
  --conf spark.executor.instances=4 \
  --conf spark.executor.cores=4 --conf spark.executor.memory=8g \
  --conf spark.dynamicAllocation.enabled=true \
  --conf spark.dynamicAllocation.shuffleTracking.enabled=true \
  --conf spark.eventLog.enabled=true \
  --conf spark.eventLog.dir=s3a://logs/spark/ \
  local:///opt/job/gold_harian.py s3a://lake
