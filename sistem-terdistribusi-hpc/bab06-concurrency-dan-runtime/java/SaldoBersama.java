// Kode 6.17: soal saldo bersama dengan virtual thread dan AtomicLong.
// Jalankan: java SaldoBersama.java
import java.util.concurrent.Executors;
import java.util.concurrent.atomic.AtomicLong;

public class SaldoBersama {
    public static void main(String[] args) {
        for (int ulang = 0; ulang < 5; ulang++) {
            AtomicLong saldo = new AtomicLong();
            long t0 = System.nanoTime();
            try (var ex = Executors.newVirtualThreadPerTaskExecutor()) {
                for (int t = 0; t < 1000; t++)
                    ex.submit(() -> {
                        for (int i = 0; i < 1000; i++) saldo.incrementAndGet();
                    });
            }
            System.out.printf("saldo=%d waktu=%.1f ms%n", saldo.get(), (System.nanoTime() - t0) / 1e6);
        }
    }
}
