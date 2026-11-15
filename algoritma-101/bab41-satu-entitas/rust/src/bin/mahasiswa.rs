// Bab 41: entitas Mahasiswa sebagai struct, JSON manual, index komposit, dan pagination.
// Tanpa crate eksternal; di proyek nyata serialization biasanya memakai serde.
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq)]
struct Mahasiswa {
    nim: String,
    nama: String,
    prodi: String,
    angkatan: u16,
    ipk: f64,
    email: String,
    hobi: Vec<String>,
}

fn esc(s: &str) -> String {
    s.replace('\\', "\\\\").replace('"', "\\\"")
}

impl Mahasiswa {
    fn lulus_syarat_beasiswa(&self) -> bool {
        self.ipk >= 3.5
    }
    // key diurutkan alfabetis, sama dengan json.dumps(sort_keys=True) di Python
    fn to_json(&self) -> String {
        let hobi: Vec<String> = self.hobi.iter().map(|h| format!("\"{}\"", esc(h))).collect();
        format!(
            "{{\"angkatan\": {}, \"email\": \"{}\", \"hobi\": [{}], \"ipk\": {}, \"nama\": \"{}\", \"nim\": \"{}\", \"prodi\": \"{}\"}}",
            self.angkatan, esc(&self.email), hobi.join(", "), self.ipk,
            esc(&self.nama), esc(&self.nim), esc(&self.prodi)
        )
    }
}

// offset: lewati page*size baris dulu; mengembalikan (hasil, baris yang disentuh)
fn page_offset(rows: &[Mahasiswa], page: usize, size: usize) -> (Vec<&str>, usize) {
    let start = (page * size).min(rows.len());
    let end = (start + size).min(rows.len());
    (rows[start..end].iter().map(|m| m.nim.as_str()).collect(), end)
}

// cursor: binary search ke nim terakhir yang sudah dilihat (rows terurut menurut nim)
fn page_cursor<'a>(rows: &'a [Mahasiswa], after: &str, size: usize) -> Vec<&'a str> {
    let start = rows.partition_point(|m| m.nim.as_str() <= after);
    rows[start..(start + size).min(rows.len())].iter().map(|m| m.nim.as_str()).collect()
}

fn main() {
    let ani = Mahasiswa {
        nim: "20271001".into(), nama: "Ani Rahma".into(), prodi: "TI".into(), angkatan: 2027,
        ipk: 3.75, email: "ani@contoh.ac.id".into(), hobi: vec!["catur".into(), "panahan".into()],
    };
    let j = ani.to_json();
    println!("{}", j);
    assert_eq!(j, r#"{"angkatan": 2027, "email": "ani@contoh.ac.id", "hobi": ["catur", "panahan"], "ipk": 3.75, "nama": "Ani Rahma", "nim": "20271001", "prodi": "TI"}"#);
    assert!(ani.lulus_syarat_beasiswa());

    let prodi = ["TI", "SI", "BD"];
    let mut rows: Vec<Mahasiswa> = (1..=1000)
        .map(|i: usize| Mahasiswa {
            nim: format!("2027{:04}", i), nama: format!("Mhs {}", i), prodi: prodi[i % 3].into(),
            angkatan: 2024 + (i % 4) as u16, ipk: 2.5 + ((i * 37) % 150) as f64 / 100.0,
            email: format!("m{}@contoh.ac.id", i), hobi: vec![],
        })
        .collect();
    rows.push(ani.clone());
    rows.sort_by(|a, b| a.nim.cmp(&b.nim));

    // index komposit (prodi, angkatan) -> daftar posisi baris
    let mut idx: BTreeMap<(String, u16), Vec<usize>> = BTreeMap::new();
    for (pos, m) in rows.iter().enumerate() {
        idx.entry((m.prodi.clone(), m.angkatan)).or_default().push(pos);
    }
    let hit = &idx[&("TI".to_string(), 2027)];
    assert!(hit.iter().all(|&p| rows[p].prodi == "TI" && rows[p].angkatan == 2027));
    println!("index (TI, 2027): {} baris", hit.len());

    let (p0, _) = page_offset(&rows, 0, 5);
    assert_eq!(p0, vec!["20270001", "20270002", "20270003", "20270004", "20270005"]);
    let (_, touched) = page_offset(&rows, 150, 5);
    assert_eq!(touched, 755); // halaman 150 menyentuh 755 baris
    let c = page_cursor(&rows, "20270750", 5);
    assert_eq!(c[0], "20270751");
    println!("offset halaman 150 menyentuh {} baris; cursor langsung ke {}", touched, c[0]);
    println!("semua uji mahasiswa lolos");
}
