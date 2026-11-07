// Total nominal per kanal dengan DataFusion (Kode 1.4, versi Rust).
use datafusion::prelude::*;

#[tokio::main]
async fn main() -> datafusion::error::Result<()> {
    let ctx = SessionContext::new();
    // daftarkan berkas Parquet sebagai tabel bernama trx
    ctx.register_parquet("trx", "../../lake/silver/transaksi.parquet",
                         ParquetReadOptions::default()).await?;
    let df = ctx
        .sql("SELECT kanal, SUM(nominal) AS total, COUNT(*) AS jml \
              FROM trx GROUP BY kanal ORDER BY total DESC")
        .await?;
    df.show().await?;
    Ok(())
}
