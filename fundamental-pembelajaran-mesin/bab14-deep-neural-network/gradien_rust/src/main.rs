// Hasil kali turunan lokal sepanjang L lapisan: rantai polos vs rantai residual.
// Polos: prod w * sigma'(z). Residual: prod (1 + w * sigma'(z)). Kode 11.6 pada buku.
fn turunan_sigmoid(z: f64) -> f64 {
    let s = 1.0 / (1.0 + (-z).exp());
    s * (1.0 - s)
}

fn main() {
    let w = 1.0; // bobot skalar tiap lapisan
    let z = 0.0; // pre-activation di titik tercuram sigmoid
    let lokal = w * turunan_sigmoid(z); // = 0.25
    for l in [5, 10, 20, 50] {
        let polos = lokal.powi(l);
        let residual = (1.0 + lokal).powi(l);
        println!("L={l:3}: polos = {polos:.3e}, residual = {residual:.3e}");
    }
    // pada residual, cabang dapat diredam (misal w kecil) tanpa memutus jalur identitas
    let lokal_kecil = 0.01 * turunan_sigmoid(z);
    println!("residual dengan cabang kecil, L=50: {:.3}", (1.0 + lokal_kecil).powi(50));
}
