"""Fitur yang sama untuk pelatihan (offline) dan serving (online) dengan Feast.

Langkah:
  python buat_data_fitur.py           # membuat feature_repo/data/fitur_rekening.parquet
  cd feature_repo && feast apply && cd ..
  python pakai_fitur.py
"""
from datetime import datetime, timezone
import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path="feature_repo")
FITUR = ["fitur_rekening:n_trx_10m", "fitur_rekening:n_perangkat_1h",
         "fitur_rekening:rata_nominal_30h"]

# 1. pelatihan: nilai fitur SEBELUM waktu setiap transaksi berlabel (point-in-time join)
label = pd.DataFrame({
    "id_rekening": ["R-10023", "R-20077"],
    "event_timestamp": pd.to_datetime(["2026-10-20 12:09", "2026-10-21 08:15"], utc=True),
    "fraud": [1, 0],
})
latih = store.get_historical_features(entity_df=label, features=FITUR).to_df()
print("== data latih (offline)\n", latih)

# 2. salin nilai terbaru ke online store (di produksi dijadwalkan Airflow)
store.materialize_incremental(end_date=datetime.now(timezone.utc))

# 3. serving: nilai terbaru satu rekening dalam milidetik
online = store.get_online_features(
    features=FITUR, entity_rows=[{"id_rekening": "R-10023"}]).to_dict()
print("== online\n", online)
