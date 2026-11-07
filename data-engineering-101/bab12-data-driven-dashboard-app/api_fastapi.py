"""API KPI dengan FastAPI.
Jalankan: python gen_gold.py && uvicorn api_fastapi:app --reload
Coba: curl localhost:8000/api/kpi/BGR   (diizinkan)
      curl localhost:8000/api/kpi/BDG   (403)
"""
import duckdb
from fastapi import Depends, FastAPI, HTTPException

app = FastAPI(title="API KPI Cabang")
con = duckdb.connect("gold.duckdb", read_only=True)


def pengguna_saat_ini() -> dict:
    # Di produksi: verifikasi token OIDC (mis. dari Keycloak) di sini.
    return {"nama": "ani", "cabang": ["BGR"]}


@app.get("/api/kpi/{cabang}")
def kpi(cabang: str, user: dict = Depends(pengguna_saat_ini)):
    if cabang not in user["cabang"]:              # row-level access
        raise HTTPException(status_code=403, detail="cabang lain")
    q = """SELECT tanggal, sum(nominal) AS nominal
           FROM fct_transaksi_harian WHERE kode_cabang = ?
           GROUP BY tanggal ORDER BY tanggal"""
    df = con.cursor().execute(q, [cabang]).df()
    df["tanggal"] = df["tanggal"].astype(str)
    return df.to_dict(orient="records")
