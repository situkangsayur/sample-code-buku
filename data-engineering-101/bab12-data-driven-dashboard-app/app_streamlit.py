"""Data app Streamlit: KPI cabang dan form pelabelan fraud.
Jalankan: python gen_gold.py && streamlit run app_streamlit.py
"""
import datetime as dt

import duckdb
import streamlit as st

st.set_page_config(page_title="KPI Cabang", layout="wide")


@st.cache_resource            # satu koneksi baca untuk semua sesi
def db():
    return duckdb.connect("gold.duckdb", read_only=True)


@st.cache_data(ttl=300)       # hasil kueri di-cache 5 menit
def harian(cabang: str, mulai, selesai):
    q = """SELECT tanggal, sum(nominal) AS nominal, max(data_per) AS data_per
           FROM fct_transaksi_harian
           WHERE kode_cabang = ? AND tanggal BETWEEN ? AND ?
           GROUP BY tanggal ORDER BY tanggal"""
    return db().cursor().execute(q, [cabang, mulai, selesai]).df()


def simpan_label(trx_id, label, alasan, analis):
    # Tabel operasional terpisah, BUKAN menimpa gold.
    # Contoh ini memakai DuckDB; di produksi gunakan PostgreSQL.
    with duckdb.connect("label_ops.duckdb") as con:
        con.execute("""CREATE TABLE IF NOT EXISTS label_fraud(
            trx_id VARCHAR, label VARCHAR, alasan VARCHAR,
            analis VARCHAR, waktu TIMESTAMP)""")
        con.execute("INSERT INTO label_fraud VALUES (?, ?, ?, ?, ?)",
                    [trx_id, label, alasan, analis, dt.datetime.now()])


# Di produksi identitas datang dari SSO di depan aplikasi.
st.session_state.setdefault("user", "analis-demo")

cabang = st.sidebar.selectbox("Cabang", ["BGR", "BDG", "DPK"])
mulai, selesai = st.sidebar.date_input(
    "Rentang tanggal", [dt.date(2026, 11, 1), dt.date(2026, 12, 28)])
df = harian(cabang, mulai, selesai)
if df.empty:
    st.warning("Tidak ada data pada rentang ini.")
    st.stop()

st.caption(f"Data per {df.data_per.max()}")
st.metric("Nominal 30 hari terakhir", f"Rp{df.nominal.tail(30).sum():,.0f}")
st.line_chart(df, x="tanggal", y="nominal")

st.subheader("Pelabelan fraud")
with st.form("label_fraud"):
    trx_id = st.text_input("ID transaksi")
    label = st.radio("Label analis", ["fraud", "bukan fraud"])
    alasan = st.text_area("Alasan singkat")
    kirim = st.form_submit_button("Simpan")

if kirim and trx_id:
    simpan_label(trx_id, label, alasan, analis=st.session_state["user"])
    st.success("Label tersimpan")
