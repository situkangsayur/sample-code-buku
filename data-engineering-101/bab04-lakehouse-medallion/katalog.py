"""Membuka katalog Iceberg untuk semua contoh Bab 4.

Bawaan: katalog SQL (SQLite) dan warehouse di folder lokal, sehingga contoh
berjalan tanpa server apa pun. Bila LAKE_CATALOG=rest, contoh memakai katalog
REST dan object storage S3 dari docker-compose.yml (lihat README.md).
"""
import os
import pathlib

from pyiceberg.catalog import load_catalog


def buka_katalog():
    if os.environ.get("LAKE_CATALOG") == "rest":
        return load_catalog("lake", **{
            "type": "rest",
            "uri": os.environ.get("REST_URI", "http://localhost:8181"),
            "s3.endpoint": os.environ.get("S3_ENDPOINT", "http://localhost:9000"),
            "s3.access-key-id": os.environ["S3_ACCESS_KEY"],
            "s3.secret-access-key": os.environ["S3_SECRET_KEY"],
            "s3.path-style-access": "true",
            "s3.region": "us-east-1",
        })
    gudang = pathlib.Path(os.environ.get("LAKE_DIR", "lake")).resolve()
    gudang.mkdir(parents=True, exist_ok=True)
    return load_catalog("lake", **{
        "type": "sql",
        "uri": f"sqlite:///{gudang}/katalog.db",
        "warehouse": f"file://{gudang}",
    })


def siapkan_namespace(cat):
    for ns in ("bronze", "silver", "gold"):
        cat.create_namespace_if_not_exists(ns)
