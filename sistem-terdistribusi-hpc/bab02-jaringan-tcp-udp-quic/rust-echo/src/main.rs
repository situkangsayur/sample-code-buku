// Kode 2.5: echo server TCP dengan Rust dan Tokio.
// Jalankan: cargo run --release    Uji: nc localhost 9000
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;

#[tokio::main]
async fn main() -> std::io::Result<()> {
    let ln = TcpListener::bind("0.0.0.0:9000").await?;
    println!("echo TCP (Tokio) mendengar di :9000");
    loop {
        let (mut sock, alamat) = ln.accept().await?;
        tokio::spawn(async move {
            // satu task ringan per klien
            let mut buf = vec![0u8; 4096];
            loop {
                let n = match sock.read(&mut buf).await {
                    Ok(0) | Err(_) => break, // 0 = klien menutup
                    Ok(n) => n,
                };
                if sock.write_all(&buf[..n]).await.is_err() {
                    break;
                }
            }
            println!("{alamat} selesai");
        });
    }
}
