// Bab 36: LZ77 naif dengan jendela 32 KiB dan panjang 3..258 (angka DEFLATE).
#[derive(Debug, PartialEq)]
enum Token {
    Lit(u8),
    Ref { jarak: usize, panjang: usize },
}

fn encode(data: &[u8]) -> Vec<Token> {
    let (window, min_m, max_m) = (32768usize, 3usize, 258usize);
    let mut out = Vec::new();
    let mut i = 0;
    while i < data.len() {
        let (mut best_j, mut best_n) = (0, 0);
        let awal = i.saturating_sub(window);
        for j in awal..i {
            let mut n = 0;
            while n < max_m && i + n < data.len() && data[j + n] == data[i + n] {
                n += 1;
            }
            if n >= best_n && n > 0 {
                best_j = j; // >= : pilih yang paling dekat
                best_n = n;
            }
        }
        if best_n >= min_m {
            out.push(Token::Ref { jarak: i - best_j, panjang: best_n });
            i += best_n;
        } else {
            out.push(Token::Lit(data[i]));
            i += 1;
        }
    }
    out
}

fn decode(token: &[Token]) -> Vec<u8> {
    let mut out: Vec<u8> = Vec::new();
    for t in token {
        match *t {
            Token::Lit(b) => out.push(b),
            Token::Ref { jarak, panjang } => {
                for _ in 0..panjang {
                    let b = out[out.len() - jarak]; // boleh tumpang tindih
                    out.push(b);
                }
            }
        }
    }
    out
}

fn main() {
    let teks = b"abrakadabra abrakadabra abrakadabra!";
    let tok = encode(teks);
    println!("{} token: {:?}", tok.len(), tok);
    assert!(tok.contains(&Token::Ref { jarak: 12, panjang: 23 }));
    assert_eq!(decode(&tok), teks.to_vec());
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn bolak_balik() {
        let data: Vec<u8> = (0..3000u32).map(|i| b"aab ca"[(i * i % 7 % 6) as usize]).collect();
        assert_eq!(decode(&encode(&data)), data);
        assert_eq!(decode(&encode(b"")), b"".to_vec());
    }
}
