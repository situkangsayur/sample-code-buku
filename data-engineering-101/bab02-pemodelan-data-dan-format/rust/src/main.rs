// Membaca metadata Parquet dengan crate parquet (Kode 2.x, versi Rust).
// Jalankan: cargo run --release -- ../data/trx.parquet
use std::fs::File;
use parquet::file::reader::{FileReader, SerializedFileReader};

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let path = std::env::args().nth(1).unwrap_or("../data/trx.parquet".into());
    let reader = SerializedFileReader::new(File::open(path)?)?;
    let md = reader.metadata();
    println!("row group: {}, baris: {}", md.num_row_groups(),
             md.file_metadata().num_rows());
    // cukup row group pertama: ukuran terkompresi tiap column chunk
    for col in md.row_group(0).columns() {
        println!("{:<14} {:?} {:>9} byte", col.column_path().string(),
                 col.compression(), col.compressed_size());
    }
    Ok(())
}
