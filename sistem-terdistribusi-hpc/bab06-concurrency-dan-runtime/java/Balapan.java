// Kode 6.1: dua thread menambah penghitung yang sama tanpa sinkronisasi.
// Jalankan: java Balapan.java   (ulangi beberapa kali, hasil berbeda-beda)
public class Balapan {
    static int n = 0;

    public static void main(String[] args) throws Exception {
        Runnable kerja = () -> {
            for (int i = 0; i < 1_000_000; i++) n++;   // tidak aman
        };
        Thread a = new Thread(kerja), b = new Thread(kerja);
        a.start(); b.start();
        a.join();  b.join();
        System.out.println(n + " (seharusnya 2000000)");
    }
}
