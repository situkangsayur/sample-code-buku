// Sengaja salah: j bertipe usize tidak pernah < 0, sehingga j -= 1 underflow.
fn insertion_sort(a: &mut [i32]) {
    for i in 1..a.len() {
        let kunci = a[i];
        let mut j = i - 1;
        while j >= 0 && a[j] > kunci {
            a[j + 1] = a[j];
            j -= 1;
        }
        a[j + 1] = kunci;
    }
}
fn main() {
    let mut a = [29, 10, 14];
    insertion_sort(&mut a);
    println!("{:?}", a);
}
