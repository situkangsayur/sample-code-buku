use datafusion::error::Result;
use datafusion::prelude::*;

#[tokio::main]
async fn main() -> Result<()> {
    // folder data dapat diberikan sebagai argumen pertama
    let base = std::env::args().nth(1).unwrap_or_else(|| "data".to_string());
    let ctx = SessionContext::new();
    ctx.register_parquet("trx", &format!("{base}/silver/transaksi/"), ParquetReadOptions::default())
        .await?;
    ctx.register_parquet("cabang", &format!("{base}/silver/cabang/"), ParquetReadOptions::default())
        .await?;
    let mulai = std::time::Instant::now();
    let df = ctx
        .sql(
            "SELECT t.tanggal, c.wilayah, c.cabang, SUM(t.nominal) AS total, \
                    COUNT(DISTINCT t.id_nasabah) AS nasabah_aktif \
             FROM trx t JOIN cabang c ON t.id_cabang = c.id_cabang \
             WHERE t.status = 'SUKSES' \
             GROUP BY t.tanggal, c.wilayah, c.cabang",
        )
        .await?;
    let hasil = df.collect().await?; // eksekusi paralel di semua core
    let baris: usize = hasil.iter().map(|b| b.num_rows()).sum();
    println!("DataFusion: {} baris dalam {:?}", baris, mulai.elapsed());
    Ok(())
}
