// Kode 10.2: consumer at-least-once dengan commit manual (rdkafka, Rust).
// Algoritma 10.1: commit sesudah diproses, pemrosesan idempotent berkunci id_trx.
//
// Variabel lingkungan opsional:
//   KAFKA_BROKER (default localhost:19092), TOPIK (default bank.transaksi)
use std::collections::HashSet;
use std::env;

use rdkafka::config::ClientConfig;
use rdkafka::consumer::{CommitMode, Consumer, StreamConsumer};
use rdkafka::Message;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let broker = env::var("KAFKA_BROKER").unwrap_or_else(|_| "localhost:19092".to_string());
    let topik = env::var("TOPIK").unwrap_or_else(|_| "bank.transaksi".to_string());

    let consumer: StreamConsumer = ClientConfig::new()
        .set("bootstrap.servers", &broker)
        .set("group.id", "fraud-rust")
        .set("enable.auto.commit", "false")     // commit manual sesudah diproses
        .set("auto.offset.reset", "earliest")
        .create()?;
    consumer.subscribe(&[topik.as_str()])?;
    println!("membaca {} dari {} (group fraud-rust)", topik, broker);

    // Pengganti tabel tujuan berkunci unik id_trx. Di produksi: UPSERT ke
    // basis data, sehingga duplikat setelah restart tetap aman.
    let mut sudah_diproses: HashSet<String> = HashSet::new();

    loop {
        let m = consumer.recv().await?;
        if let Some(Ok(isi)) = m.payload_view::<str>() {
            let key = m.key().map(|k| String::from_utf8_lossy(k).to_string());
            let id_trx = serde_json::from_str::<serde_json::Value>(isi)
                .ok()
                .and_then(|v| v.get("id_trx").and_then(|x| x.as_str()).map(String::from));
            match id_trx {
                Some(id) if sudah_diproses.contains(&id) => {
                    // duplikat dari retry atau restart: lewati
                    println!("p{} off{} duplikat {} dilewati", m.partition(), m.offset(), id);
                }
                Some(id) => {
                    // proses idempotent, misalnya UPSERT berkunci id_trx
                    println!("p{} off{} key={:?} {}", m.partition(), m.offset(), key, isi);
                    sudah_diproses.insert(id);
                }
                None => eprintln!("p{} off{} pesan tanpa id_trx: {}", m.partition(), m.offset(), isi),
            }
        }
        // commit sesudah diproses: bila mati sebelum baris ini, pesan dibaca ulang
        consumer.commit_message(&m, CommitMode::Async)?;
    }
}
