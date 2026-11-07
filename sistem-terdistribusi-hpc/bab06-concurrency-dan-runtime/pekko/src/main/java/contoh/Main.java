// Soal saldo bersama dengan actor: 1.000 pengirim x 1.000 pesan Tambah.
// Setiap pengirim mengirim Ambil SETELAH semua Tambah-nya. Urutan pesan dari satu
// pengirim ke satu penerima dijamin, sehingga balasan Ambil yang diproses paling akhir
// sudah melihat semua Tambah; nilai maksimum balasan = hasil akhir.
// Jalankan: sbt run
package contoh;

import org.apache.pekko.actor.typed.ActorRef;
import org.apache.pekko.actor.typed.ActorSystem;
import org.apache.pekko.actor.typed.Behavior;
import org.apache.pekko.actor.typed.javadsl.Behaviors;

public class Main {
    static final int PENGIRIM = 1000, PER_PENGIRIM = 1000;

    // pengumpul balasan: menunggu 1.000 balasan lalu mencetak nilai terbesar
    static Behavior<Integer> pengumpul(int sisa, int maks, long t0) {
        return Behaviors.receive((ctx, n) -> {
            int m = Math.max(maks, n);
            if (sisa == 1) {
                System.out.printf("saldo=%d waktu=%.1f ms%n", m, (System.nanoTime() - t0) / 1e6);
                ctx.getSystem().terminate();
                return Behaviors.stopped();
            }
            return pengumpul(sisa - 1, m, t0);
        });
    }

    static Behavior<Void> utama() {
        return Behaviors.setup(ctx -> {
            long t0 = System.nanoTime();
            ActorRef<Penghitung.Pesan> hitung = ctx.spawn(Penghitung.aman(), "penghitung");
            ActorRef<Integer> kumpul = ctx.spawn(pengumpul(PENGIRIM, 0, t0), "pengumpul");
            for (int p = 0; p < PENGIRIM; p++) {
                ctx.spawn(Behaviors.<Void>setup(c -> {
                    for (int i = 0; i < PER_PENGIRIM; i++) hitung.tell(Penghitung.Tambah.INSTANCE);
                    hitung.tell(new Penghitung.Ambil(kumpul));
                    return Behaviors.stopped();
                }), "pengirim-" + p);
            }
            return Behaviors.empty();
        });
    }

    public static void main(String[] args) {
        ActorSystem.create(utama(), "saldo");
    }
}
