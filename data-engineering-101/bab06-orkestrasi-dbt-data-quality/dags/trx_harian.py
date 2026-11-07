"""DAG harian bronze -> silver -> gold (Airflow 3.x, TaskFlow API).

Setiap run membawa tanggal logisnya sendiri ({{ ds }}): run untuk 2026-11-03
selalu mengolah data 2026-11-03, kapan pun ia dijalankan (backfill aman).

Catatan Airflow 3: schedule="@daily" kini memakai CronTriggerTimetable
([scheduler] create_cron_data_intervals = False), sehingga ds = tanggal saat run
dipicu. Agar ds menunjuk hari yang datanya sudah lengkap (awal data interval),
DAG ini memakai CronDataIntervalTimetable secara eksplisit.
Variabel lingkungan:
  PROYEK_DIR  folder bab06 (berisi siapkan_bronze.py dan dbt_bank/)
  PY_BIN      folder bin virtualenv yang berisi python dan dbt
"""
import os

import pendulum
from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import CronDataIntervalTimetable, dag, task

PROYEK = os.environ.get("PROYEK_DIR", "/opt/proyek")
BIN = os.environ.get("PY_BIN", "/usr/local/bin")
DBT = f"cd {PROYEK}/dbt_bank && {BIN}/dbt"
VARS = "--profiles-dir . --vars '{tgl: {{ ds }}}'"


@dag(schedule=CronDataIntervalTimetable("0 0 * * *", timezone="Asia/Jakarta"),
     start_date=pendulum.datetime(2026, 11, 1, tz="Asia/Jakarta"),
     catchup=True,                      # hari yang terlewat ikut dijalankan
     max_active_runs=2,                 # batasi paralelisme backfill
     default_args={"retries": 2, "retry_delay": pendulum.duration(minutes=5)},
     tags=["bank-syariah", "medallion"])
def trx_harian():

    @task.bash
    def ingest_bronze(ds=None) -> str:
        # menimpa partisi tgl=ds secara utuh: idempotent
        return f"cd {PROYEK} && {BIN}/python siapkan_bronze.py {ds}"

    snapshot = BashOperator(task_id="dbt_snapshot", bash_command=f"{DBT} snapshot {VARS}")
    # dbt build = run + test berurutan; test gagal -> model turunan (gold) di-skip
    build = BashOperator(task_id="dbt_build", bash_command=f"{DBT} build {VARS}")

    ingest_bronze() >> snapshot >> build


trx_harian()
