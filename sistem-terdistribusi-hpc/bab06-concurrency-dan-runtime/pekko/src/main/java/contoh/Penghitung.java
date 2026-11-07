// Kode 6.9: actor penghitung bertipe dengan supervision (Java, Apache Pekko).
package contoh;

import org.apache.pekko.actor.typed.ActorRef;
import org.apache.pekko.actor.typed.Behavior;
import org.apache.pekko.actor.typed.SupervisorStrategy;
import org.apache.pekko.actor.typed.javadsl.Behaviors;

public class Penghitung {
    public interface Pesan {}
    public enum Tambah implements Pesan { INSTANCE }
    public record Ambil(ActorRef<Integer> balas) implements Pesan {}

    // state n tidak disimpan di variabel bersama: ia "dibawa" oleh behavior
    public static Behavior<Pesan> create(int n) {
        return Behaviors.receive(Pesan.class)
            .onMessageEquals(Tambah.INSTANCE, () -> create(n + 1))
            .onMessage(Ambil.class, m -> {
                m.balas().tell(n);               // balas tanpa menunggu
                return Behaviors.same();
            })
            .build();
    }

    // dibungkus supervisor: mulai ulang dengan state awal bila gagal
    public static Behavior<Pesan> aman() {
        return Behaviors.supervise(create(0))
            .onFailure(Exception.class, SupervisorStrategy.restart());
    }
}
