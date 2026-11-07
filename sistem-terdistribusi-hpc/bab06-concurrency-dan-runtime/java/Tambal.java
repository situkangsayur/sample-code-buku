// Kode 6.2: tiga cara membuat penambahan aman, plus pengukuran waktu.
// Jalankan: java Tambal.java [jumlahThread]   (default 8)
import java.util.concurrent.atomic.AtomicInteger;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

public class Tambal {
    interface Penghitung { void tambah(); int nilai(); }

    // 1. synchronized: lock melekat pada objek
    static class PenghitungSync implements Penghitung {
        private int n = 0;
        public synchronized void tambah() { n++; }
        public synchronized int nilai() { return n; }
    }
    // 2. ReentrantLock: lebih fleksibel (tryLock, fairness)
    static class PenghitungLock implements Penghitung {
        private final Lock kunci = new ReentrantLock();
        private int n = 0;
        public void tambah() {
            kunci.lock();
            try { n++; } finally { kunci.unlock(); }   // unlock WAJIB di finally
        }
        public int nilai() { kunci.lock(); try { return n; } finally { kunci.unlock(); } }
    }
    // 3. AtomicInteger: tanpa lock, memakai compare-and-swap CPU
    static class PenghitungAtomik implements Penghitung {
        private final AtomicInteger n = new AtomicInteger();
        public void tambah() { n.incrementAndGet(); }
        public int nilai() { return n.get(); }
    }

    static void ukur(String nama, Penghitung p, int jThread, int perThread) throws Exception {
        Thread[] ts = new Thread[jThread];
        long t0 = System.nanoTime();
        for (int i = 0; i < jThread; i++) {
            ts[i] = new Thread(() -> { for (int k = 0; k < perThread; k++) p.tambah(); });
            ts[i].start();
        }
        for (Thread t : ts) t.join();
        long ms = (System.nanoTime() - t0) / 1_000_000;
        System.out.printf("%-14s thread=%-4d hasil=%d (harus %d) waktu=%d ms%n",
                nama, jThread, p.nilai(), jThread * perThread, ms);
    }

    public static void main(String[] args) throws Exception {
        int j = args.length > 0 ? Integer.parseInt(args[0]) : 8;
        int per = 8_000_000 / j;
        ukur("synchronized", new PenghitungSync(), j, per);
        ukur("ReentrantLock", new PenghitungLock(), j, per);
        ukur("AtomicInteger", new PenghitungAtomik(), j, per);
    }
}
