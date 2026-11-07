"""Mengirim satu event OpenLineage COMPLETE ke Marquez.
Jalankan Marquez lebih dulu (lihat README), lalu: python openlineage_event.py
"""
import json
import os
import urllib.request
import uuid
from datetime import datetime, timezone

MARQUEZ = os.environ.get("MARQUEZ_URL", "http://localhost:5000")

event = {
    "eventType": "COMPLETE",
    "eventTime": datetime.now(timezone.utc).isoformat(),
    "run": {"runId": str(uuid.uuid4())},
    "job": {"namespace": "bank-syariah", "name": "gold.volume_cabang"},
    "inputs": [{"namespace": "iceberg", "name": "silver.transaksi"},
               {"namespace": "iceberg", "name": "silver.rekening"}],
    "outputs": [{"namespace": "iceberg", "name": "gold.volume_cabang"}],
    "producer": "https://contoh.bank/pipeline",
    "schemaURL": "https://openlineage.io/spec/2-0-2/OpenLineage.json#/$defs/RunEvent",
}
req = urllib.request.Request(f"{MARQUEZ}/api/v1/lineage",
                             data=json.dumps(event).encode(),
                             headers={"Content-Type": "application/json"})
print(urllib.request.urlopen(req).status)
