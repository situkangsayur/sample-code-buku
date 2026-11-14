// Bab 3: simulator Enigma I (rotor I-V, reflector B, plugboard).
// Huruf dinyatakan sebagai angka 0..25 (A = 0).

const ROTOR: [(&str, u8); 5] = [
    ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", b'Q'), // I
    ("AJDKSIRUXBLHWTMCQGZNPYFVOE", b'E'), // II
    ("BDFHJLCPRTXVZNYEIWGAKMUSQO", b'V'), // III
    ("ESOVPZJAYQUIRHXLNFTGKDCMWB", b'J'), // IV
    ("VZBRGITYUPSDNHLXAWMJQOFECK", b'Z'), // V
];
const REFLECTOR_B: &str = "YRUHQSLDPXNGOKMIEBFZCWVJAT";

fn idx(c: u8) -> usize {
    (c - b'A') as usize
}

struct Enigma {
    maju: [[usize; 26]; 3],
    mundur: [[usize; 26]; 3],
    takik: [usize; 3],
    cincin: [usize; 3],
    pos: [usize; 3], // 0 = kiri, 2 = kanan (rotor cepat)
    plug: [usize; 26],
    refl: [usize; 26],
}

impl Enigma {
    fn new(urutan: [usize; 3], cincin: &str, posisi: &str, colokan: &str) -> Self {
        let mut e = Enigma {
            maju: [[0; 26]; 3], mundur: [[0; 26]; 3], takik: [0; 3],
            cincin: [0; 3], pos: [0; 3], plug: [0; 26], refl: [0; 26],
        };
        for k in 0..3 {
            let (w, t) = ROTOR[urutan[k] - 1];
            for (i, c) in w.bytes().enumerate() {
                e.maju[k][i] = idx(c);
                e.mundur[k][idx(c)] = i;
            }
            e.takik[k] = idx(t);
            e.cincin[k] = idx(cincin.as_bytes()[k]);
            e.pos[k] = idx(posisi.as_bytes()[k]);
        }
        for i in 0..26 { e.plug[i] = i; }
        for p in colokan.split_whitespace() {
            let (x, y) = (idx(p.as_bytes()[0]), idx(p.as_bytes()[1]));
            e.plug[x] = y;
            e.plug[y] = x;
        }
        for (i, c) in REFLECTOR_B.bytes().enumerate() { e.refl[i] = idx(c); }
        e
    }

    // Rotor berputar sebelum huruf disandikan, termasuk double stepping.
    fn langkah(&mut self) {
        if self.pos[1] == self.takik[1] {
            self.pos[1] = (self.pos[1] + 1) % 26;
            self.pos[0] = (self.pos[0] + 1) % 26;
        } else if self.pos[2] == self.takik[2] {
            self.pos[1] = (self.pos[1] + 1) % 26;
        }
        self.pos[2] = (self.pos[2] + 1) % 26;
    }

    fn lewat(&self, x: usize, k: usize, maju: bool) -> usize {
        let geser = (self.pos[k] + 26 - self.cincin[k]) % 26;
        let t = if maju { &self.maju[k] } else { &self.mundur[k] };
        (t[(x + geser) % 26] + 26 - geser) % 26
    }

    fn huruf(&mut self, c: u8) -> u8 {
        self.langkah();
        let mut x = self.plug[idx(c)];
        for k in [2, 1, 0] { x = self.lewat(x, k, true); }
        x = self.refl[x];
        for k in [0, 1, 2] { x = self.lewat(x, k, false); }
        b'A' + self.plug[x] as u8
    }

    fn sandi(&mut self, teks: &str) -> String {
        teks.bytes().filter(|c| c.is_ascii_uppercase()).map(|c| self.huruf(c) as char).collect()
    }
}

fn main() {
    let hasil = Enigma::new([1, 2, 3], "AAA", "AAA", "").sandi("AAAAA");
    println!("AAAAA -> {}", hasil); // BDZGO
    assert_eq!(hasil, "BDZGO");
    let colokan = "AV BS CG DL FU HZ IN KM OW RX";
    let s = Enigma::new([2, 4, 5], "BUL", "RTZ", colokan).sandi("WETTERVORHERSAGEFUERDIENORDSEE");
    println!("{}", s);
    assert_eq!(s, "ZCUJRURDYIQKTNQVJMXZHLWPYZQLZM"); // sama dengan versi Python
    println!("semua uji lolos");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reciprocal_dan_tidak_ke_diri_sendiri() {
        let colokan = "AV BS CG DL FU HZ IN KM OW RX";
        let asli = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".repeat(20);
        let s = Enigma::new([2, 4, 5], "BUL", "RTZ", colokan).sandi(&asli);
        assert!(asli.bytes().zip(s.bytes()).all(|(a, b)| a != b));
        let balik = Enigma::new([2, 4, 5], "BUL", "RTZ", colokan).sandi(&s);
        assert_eq!(balik, asli);
    }

    #[test]
    fn double_stepping() {
        let mut e = Enigma::new([1, 2, 3], "AAA", "ADU", "");
        let mut jejak = Vec::new();
        for _ in 0..3 {
            e.langkah();
            jejak.push(e.pos.iter().map(|&p| (b'A' + p as u8) as char).collect::<String>());
        }
        assert_eq!(jejak, ["ADV", "AEW", "BFX"]);
    }
}
