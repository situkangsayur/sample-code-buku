// Kode 6.3 dan 6.4: deadlock karena urutan lock terbalik, dan perbaikannya.
// Jalankan: java Deadlock.java macet    (program menggantung; cek dengan jstack <pid>)
//           java Deadlock.java urut     (urutan lock global, selesai normal)
public class Deadlock {
    static class Rekening {
        final int id; long saldo;
        Rekening(int id, long saldo) { this.id = id; this.saldo = saldo; }
    }

    static void tidur(long ms) { try { Thread.sleep(ms); } catch (InterruptedException e) { } }

    // versi berbahaya: kunci "dari" dulu, lalu "ke"
    static void transferMacet(Rekening dari, Rekening ke, long jumlah) {
        synchronized (dari) {
            tidur(50);
            synchronized (ke) { dari.saldo -= jumlah; ke.saldo += jumlah; }
        }
    }

    // versi aman: selalu kunci id terkecil lebih dulu (mematahkan circular wait)
    static void transfer(Rekening dari, Rekening ke, long jumlah) {
        Rekening pertama = dari.id < ke.id ? dari : ke;
        Rekening kedua   = dari.id < ke.id ? ke : dari;
        synchronized (pertama) {
            tidur(50);
            synchronized (kedua) { dari.saldo -= jumlah; ke.saldo += jumlah; }
        }
    }

    public static void main(String[] args) throws Exception {
        boolean macet = args.length > 0 && args[0].equals("macet");
        Rekening a = new Rekening(1, 1000), b = new Rekening(2, 1000);
        Thread t1 = new Thread(() -> { if (macet) transferMacet(a, b, 100); else transfer(a, b, 100); });
        Thread t2 = new Thread(() -> { if (macet) transferMacet(b, a, 50);  else transfer(b, a, 50); });
        t1.start(); t2.start();
        t1.join(3000); t2.join(3000);
        if (t1.isAlive() || t2.isAlive()) {
            System.out.println("DEADLOCK: kedua thread masih menunggu. Jalankan jstack <pid> untuk melihatnya.");
            System.exit(1);
        }
        System.out.println("selesai: A=" + a.saldo + " B=" + b.saldo + " total=" + (a.saldo + b.saldo));
    }
}
