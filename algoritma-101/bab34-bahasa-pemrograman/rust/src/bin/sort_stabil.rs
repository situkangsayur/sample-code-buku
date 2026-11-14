// Bab 34: sort stabil (driftsort) dan tidak stabil (ipnsort) di Rust 1.81+.
// f64 tidak mengimplementasikan Ord, jadi dipakai total_cmp.

fn main() {
    let mhs = vec![("Ani", 80), ("Budi", 75), ("Citra", 80), ("Dewi", 75), ("Eka", 90)];

    let mut stabil = mhs.clone();
    stabil.sort_by_key(|&(_, nilai)| nilai); // stabil: urutan nama dijaga
    println!("{:?}", stabil);
    assert_eq!(
        stabil,
        vec![("Budi", 75), ("Dewi", 75), ("Ani", 80), ("Citra", 80), ("Eka", 90)]
    );

    let mut cepat = mhs.clone();
    cepat.sort_unstable_by_key(|&(_, nilai)| nilai); // urutan nilai benar
    let nilai: Vec<i32> = cepat.iter().map(|&(_, n)| n).collect();
    assert_eq!(nilai, vec![75, 75, 80, 80, 90]);

    let mut ipk = vec![3.5_f64, 2.75, 3.9, 3.0];
    ipk.sort_by(|a, b| a.total_cmp(b)); // ipk.sort() tidak dikompilasi
    assert_eq!(ipk, vec![2.75, 3.0, 3.5, 3.9]);
    println!("{:?}", ipk);
}
