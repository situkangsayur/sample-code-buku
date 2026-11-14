// Ruang kunci Enigma tiga rotor dari lima, plugboard 10 kabel (Kode 32.1 versi Rust).
// Ring setting dan reflektor tidak dihitung, sama dengan versi Python.

fn faktorial(n: u128) -> u128 {
    (1..=n).product()
}

fn plugboard(kabel: u128) -> u128 {
    faktorial(26) / (faktorial(26 - 2 * kabel) * faktorial(kabel) * (1u128 << kabel))
}

fn main() {
    let urutan = 5 * 4 * 3u128;
    let posisi = 26u128.pow(3);
    let papan = plugboard(10);
    let total = urutan * posisi * papan;
    println!("{} x {} x {} = {}", urutan, posisi, papan, total);
    assert_eq!(papan, 150_738_274_937_250);
    assert_eq!(total, 158_962_555_217_826_360_000);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn plugboard_kecil() {
        assert_eq!(plugboard(0), 1);
        assert_eq!(plugboard(1), 325); // C(26,2)
    }
}
