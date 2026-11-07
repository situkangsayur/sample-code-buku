// Kode 2.4: Find-S dalam Rust, hanya pustaka standar.
// None = batasan kosong, Some("?") = apa saja, Some(nilai) = nilai tertentu.
fn find_s<'a>(data: &[(Vec<&'a str>, bool)]) -> Vec<Option<&'a str>> {
    let n = data[0].0.len();
    let mut h: Vec<Option<&str>> = vec![None; n]; // paling khusus
    for (x, positif) in data {
        if !*positif {
            continue; // contoh negatif diabaikan
        }
        for i in 0..n {
            h[i] = match h[i] {
                None => Some(x[i]),
                Some(c) if c == x[i] || c == "?" => Some(c),
                Some(_) => Some("?"), // longgarkan seminimal mungkin
            };
        }
    }
    h
}

fn main() {
    let data = vec![
        (vec!["Sunny", "Warm", "Normal", "Strong", "Warm", "Same"], true),
        (vec!["Sunny", "Warm", "High", "Strong", "Warm", "Same"], true),
        (vec!["Rainy", "Cold", "High", "Strong", "Warm", "Change"], false),
        (vec!["Sunny", "Warm", "High", "Strong", "Cool", "Change"], true),
    ];
    let h = find_s(&data);
    let teks: Vec<&str> = h.iter().map(|c| c.unwrap_or("0")).collect();
    println!("h = <{}>", teks.join(", "));
}
