// Agregasi transaksi per kanal dengan DataFusion (Rust), membaca Parquet bronze.
// Jalankan dari folder bab05-etl-satu-mesin:  cargo run --release --manifest-path datafusion-rust/Cargo.toml
use datafusion::error::Result;
use datafusion::functions_aggregate::expr_fn::count;
use datafusion::prelude::*;

#[tokio::main]
async fn main() -> Result<()> {
    let ctx = SessionContext::new();
    // daftarkan seluruh folder sebagai satu tabel; kolom partisi tanggal ikut terbaca
    let opsi = ParquetReadOptions::default()
        .table_partition_cols(vec![("tanggal".to_string(), datafusion::arrow::datatypes::DataType::Utf8)]);
    ctx.register_parquet("trx", "data/bronze/trx/", opsi).await?;

    // SQL: rencana dioptimalkan (projection dan predicate pushdown) lalu dieksekusi paralel
    let df = ctx
        .sql("SELECT upper(kanal) AS kanal, count(*) AS n, \
              sum(TRY_CAST(nominal AS BIGINT)) AS total \
              FROM trx WHERE tanggal >= '2026-11-03' \
              GROUP BY 1 ORDER BY total DESC")
        .await?;
    df.show().await?;

    // DataFrame API: kueri yang sama tanpa SQL
    let df2 = ctx
        .table("trx")
        .await?
        .filter(col("tanggal").gt_eq(lit("2026-11-03")))?
        .aggregate(vec![upper(col("kanal")).alias("kanal")], vec![count(lit(1)).alias("n")])?;
    df2.show().await?;
    Ok(())
}
