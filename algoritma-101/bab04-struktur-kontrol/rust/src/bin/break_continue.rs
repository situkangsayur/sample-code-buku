// Algoritma 4.6 KelipatanTujuhPertama, ditambah contoh label pada loop bersarang.
fn kelipatan_tujuh_pertama(a: &[i64]) -> i64 {
    let mut hasil = 0;
    for &x in a {
        if x <= 0 {
            continue; // lewati bilangan nol dan negatif
        }
        if x % 7 == 0 {
            hasil = x;
            break; // sudah ketemu
        }
    }
    hasil
}

// break berlabel: keluar dari dua loop sekaligus
fn pasangan_pertama(jumlah: u32) -> Option<(u32, u32)> {
    let mut hasil = None;
    'luar: for i in 1..10 {
        for j in i..10 {
            if i * j == jumlah {
                hasil = Some((i, j));
                break 'luar;
            }
        }
    }
    hasil
}

fn main() {
    assert_eq!(kelipatan_tujuh_pertama(&[5, -14, 0, 21, 35]), 21);
    assert_eq!(kelipatan_tujuh_pertama(&[-7, 3, 14, 0, 28]), 14);
    assert_eq!(kelipatan_tujuh_pertama(&[]), 0);
    assert_eq!(pasangan_pertama(12), Some((2, 6)));
    println!("break_continue: semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn tidak_ada() {
        assert_eq!(kelipatan_tujuh_pertama(&[1, 2, 3]), 0);
        assert_eq!(pasangan_pertama(97), None);
    }
}
