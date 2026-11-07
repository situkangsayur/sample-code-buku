package bab13

import org.apache.pekko.actor.typed.{ActorRef, Behavior}
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import org.apache.pekko.cluster.sharding.typed.scaladsl.EntityTypeKey

// Penanda: pesan yang melintasi node diserialisasi dengan Jackson CBOR (lihat application.conf)
trait CborSerializable

// Satu entity actor per nomor rekening. Keadaan (saldo) hanya diubah oleh actor ini,
// satu pesan pada satu waktu: tidak ada lock.
object Rekening {
  sealed trait Perintah extends CborSerializable
  final case class Setor(jumlah: Long, balas: ActorRef[Saldo]) extends Perintah
  final case class Tanya(balas: ActorRef[Saldo]) extends Perintah
  final case class Saldo(id: String, nilai: Long, node: String) extends CborSerializable

  val TypeKey: EntityTypeKey[Perintah] = EntityTypeKey[Perintah]("Rekening")

  def apply(id: String): Behavior[Perintah] = Behaviors.setup { ctx =>
    val node = ctx.system.address.toString
    ctx.log.info(s"entity $id hidup di $node")
    aktif(id, 0L, node)
  }

  private def aktif(id: String, saldo: Long, node: String): Behavior[Perintah] =
    Behaviors.receiveMessage {
      case Setor(j, balas) =>
        val baru = saldo + j
        balas ! Saldo(id, baru, node)
        aktif(id, baru, node)            // keadaan baru = behavior baru
      case Tanya(balas) =>
        balas ! Saldo(id, saldo, node)
        Behaviors.same
    }
}
