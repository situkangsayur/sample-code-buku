// Kode 1.3: actor penghitung tanpa lock dengan Apache Pekko (Scala 3).
import org.apache.pekko.actor.typed.{ActorRef, ActorSystem, Behavior}
import org.apache.pekko.actor.typed.scaladsl.Behaviors

object Penghitung {
  sealed trait Pesan
  case object Tambah extends Pesan
  final case class Ambil(balas: ActorRef[Int]) extends Pesan

  def apply(n: Int = 0): Behavior[Pesan] =
    Behaviors.receiveMessage {
      case Tambah       => apply(n + 1) // keadaan baru = perilaku baru
      case Ambil(balas) =>
        balas ! n                       // kirim nilai lewat pesan
        Behaviors.same
    }
}

object Utama {
  sealed trait Perintah
  final case class Hasil(n: Int) extends Perintah

  def apply(): Behavior[Perintah] = Behaviors.setup { ctx =>
    val penghitung = ctx.spawn(Penghitung(), "penghitung")
    // 1000 pesan dikirim; actor memprosesnya satu per satu, tanpa race condition
    (1 to 1000).foreach(_ => penghitung ! Penghitung.Tambah)
    val adaptor = ctx.messageAdapter[Int](Hasil.apply)
    penghitung ! Penghitung.Ambil(adaptor)
    Behaviors.receiveMessage { case Hasil(n) =>
      ctx.log.info(s"nilai penghitung = $n")
      Behaviors.stopped
    }
  }

  @main def jalankan(): Unit = ActorSystem(Utama(), "contoh")
}
