// Kode 6.5: thread pool klasik vs virtual thread untuk 10.000 tugas I/O (Java 21+).
// Jalankan: java VirtualThreads.java
import java.time.Duration;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.stream.IntStream;

public class VirtualThreads {
    static long jalankan(ExecutorService exec, int n) {
        long t0 = System.nanoTime();
        try (exec) {
            IntStream.range(0, n).forEach(i -> exec.submit(() -> {
                Thread.sleep(Duration.ofSeconds(1));   // pura-pura menunggu I/O
                return i;
            }));
        }   // close() menunggu semua tugas selesai
        return (System.nanoTime() - t0) / 1_000_000;
    }

    public static void main(String[] args) {
        System.out.println("virtual thread, 10.000 tugas: "
                + jalankan(Executors.newVirtualThreadPerTaskExecutor(), 10_000) + " ms");
        // thread pool 200 thread OS: 10.000 tugas x 1 s / 200 = sekitar 50 s; kita pakai 1.000 tugas
        System.out.println("fixed pool 200, 1.000 tugas : "
                + jalankan(Executors.newFixedThreadPool(200), 1_000) + " ms");
    }
}
