// Membangkitkan kode Rust dari kontrak yang sama dengan server Go.
fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Pakai protoc bawaan crate protoc-bin-vendored bila PROTOC belum diatur.
    if std::env::var_os("PROTOC").is_none() {
        std::env::set_var("PROTOC", protoc_bin_vendored::protoc_bin_path()?);
    }
    tonic_build::configure()
        .build_server(false) // cukup klien
        .compile_protos(
            &["../go-katalog/proto/katalog/v1/katalog.proto"],
            &["../go-katalog/proto"],
        )?;
    Ok(())
}
