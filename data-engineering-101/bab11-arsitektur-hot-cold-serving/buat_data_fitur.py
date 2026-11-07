"""Membangkitkan tabel fitur sintetis untuk offline store Feast (Kode 11.9).
Di produksi tabel ini ditulis job Spark ke Iceberg/Parquet."""
from pathlib import Path
import numpy as np
import pandas as pd

rng = np.random.default_rng(11)
waktu = pd.date_range("2026-10-19", "2026-10-22", freq="15min", tz="UTC")
baris = []
for rek in ["R-10023", "R-20077", "R-30011"]:
    for t in waktu:
        baris.append({"id_rekening": rek, "event_time": t,
                      "n_trx_10m": int(rng.poisson(1.2)),
                      "n_perangkat_1h": int(rng.integers(1, 3)),
                      "rata_nominal_30h": float(rng.normal(350_000, 50_000))})
df = pd.DataFrame(baris)
df["n_trx_10m"] = df["n_trx_10m"].astype("int64")
df["n_perangkat_1h"] = df["n_perangkat_1h"].astype("int64")
df["rata_nominal_30h"] = df["rata_nominal_30h"].astype("float32")
tujuan = Path(__file__).with_name("feature_repo") / "data" / "fitur_rekening.parquet"
tujuan.parent.mkdir(parents=True, exist_ok=True)
df.to_parquet(tujuan, index=False)
print(f"{len(df)} baris -> {tujuan}")
