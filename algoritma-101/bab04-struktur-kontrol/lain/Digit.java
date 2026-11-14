// Padanan Java untuk Kode 4.4: do-while (Algoritma 4.5 BanyakDigit).
public class Digit {
    static int banyakDigit(int n) {
        int d = 0;
        do {
            n = n / 10;
            d = d + 1;
        } while (n != 0);   // syarat lanjut = not (n == 0)
        return d;
    }

    public static void main(String[] args) {
        if (banyakDigit(2026) != 4 || banyakDigit(0) != 1) {
            throw new AssertionError("uji gagal");
        }
        System.out.println("Digit.java: semua uji lolos");
    }
}
