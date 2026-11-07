// Klien gRPC unary dengan Rust dan tonic, memakai berkas .proto yang sama
// dengan server Go (go-katalog/proto/katalog/v1/katalog.proto).
//
// Jalankan server dulu: (cd ../go-katalog && go run ./grpcserver)
// lalu: cargo run            atau  cargo run -- 99   (ID lain)
pub mod katalogv1 { tonic::include_proto!("katalog.v1"); }   // hasil build.rs
use katalogv1::{katalog_client::KatalogClient, AmbilProdukRequest};
use std::time::Duration;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let id: i64 = std::env::args().nth(1).map(|s| s.parse()).transpose()?.unwrap_or(42);
    let mut klien = KatalogClient::connect("http://127.0.0.1:50051").await?;
    let mut req = tonic::Request::new(AmbilProdukRequest { id });
    req.set_timeout(Duration::from_millis(300));                 // deadline
    req.metadata_mut().insert("authorization", "Bearer rahasia".parse()?);
    match klien.ambil_produk(req).await {
        Ok(r) => println!("{} {}", r.get_ref().nama, r.get_ref().harga),
        // deadline yang habis di sisi klien dilaporkan tonic sebagai Cancelled
        Err(s) if matches!(s.code(), tonic::Code::DeadlineExceeded
                                   | tonic::Code::Cancelled) => println!("terlalu lambat"),
        Err(s) => println!("gagal: {}", s.message()),
    }
    Ok(())
}
