package bab13

import scala.concurrent.duration._
import scala.util.{Failure, Success}
import com.typesafe.config.ConfigFactory
import org.apache.pekko.actor.typed.{ActorSystem, Scheduler}
import org.apache.pekko.actor.typed.scaladsl.Behaviors
import org.apache.pekko.cluster.sharding.typed.scaladsl.{ClusterSharding, Entity}
import org.apache.pekko.util.Timeout

// Pemakaian: sbt "run 25520"  (node pertama/seed), lalu di terminal lain sbt "run 25521"
// Node dengan argumen kedua "kirim" juga mengirim setoran ke beberapa rekening.
object Main {
  def main(args: Array[String]): Unit = {
    val port  = args.headOption.getOrElse("25520")
    val kirim = args.lift(1).contains("kirim")
    val config = ConfigFactory
      .parseString(s"pekko.remote.artery.canonical.port=$port")
      .withFallback(ConfigFactory.load())
    implicit val system: ActorSystem[Nothing] =
      ActorSystem(Behaviors.empty[Nothing], "BankKlaster", config)

    // Daftarkan tipe entity: sharding yang memutuskan di node mana tiap entity hidup
    val sharding = ClusterSharding(system)
    sharding.init(Entity(Rekening.TypeKey)(ctx => Rekening(ctx.entityId)))

    if (kirim) {
      implicit val timeout: Timeout = 5.seconds
      implicit val sch: Scheduler = system.scheduler
      import system.executionContext
      system.scheduler.scheduleWithFixedDelay(5.seconds, 3.seconds) { () =>
        for (no <- Seq("123", "456", "789")) {
          val ref = sharding.entityRefFor(Rekening.TypeKey, no) // cukup sebut ID
          ref.ask[Rekening.Saldo](balas => Rekening.Setor(100, balas)).onComplete {
            case Success(s) => println(s"rekening ${s.id}: saldo ${s.nilai} (di ${s.node})")
            case Failure(e) => println(s"rekening $no: gagal ${e.getMessage}")
          }
        }
      }
    }
  }
}
