// Bab 3: ruang kunci Enigma I dengan u128 (u64 tidak cukup).

fn faktorial(n: u128) -> u128 {
    (1..=n).product()
}

/// n! / ((n - 2p)! * p! * 2^p)
fn colokan(p: u128) -> u128 {
    faktorial(26) / (faktorial(26 - 2 * p) * faktorial(p) * 2u128.pow(p as u32))
}

fn main() {
    let urutan: u128 = 5 * 4 * 3;
    let posisi: u128 = 26u128.pow(3);
    let cincin: u128 = 26u128.pow(2);
    let plug = colokan(10);
    let total = urutan * posisi * cincin * plug;
    println!("colokan 10 kabel: {}", plug); // 150738274937250
    println!("total kunci     : {}", total); // 107458687327250619360000
    assert_eq!(plug, 150_738_274_937_250);
    assert_eq!(urutan * posisi * plug, 158_962_555_217_826_360_000);
    assert_eq!(total, 107_458_687_327_250_619_360_000);
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn satu_kabel() {
        assert_eq!(colokan(1), 325); // C(26, 2)
        assert_eq!(colokan(0), 1);
    }
}
