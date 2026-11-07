// Kode 10.10: aturan fraud dalam Scala dengan sink Kafka.
// Membaca CDC bank.public.transaksi, menghitung window 1 menit dengan
// watermark 2 menit, lalu menulis peringatan ke topik bank.peringatan.
//
// Argumen opsional: <broker> <akar-checkpoint>
//   default: localhost:19092  s3a://lake/ckpt
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._
import org.apache.spark.sql.streaming.Trigger
import org.apache.spark.sql.types._

object FraudStream {
  def main(args: Array[String]): Unit = {
    val broker = if (args.length > 0) args(0) else "localhost:19092"
    val ckpt   = if (args.length > 1) args(1) else "s3a://lake/ckpt"

    val spark = SparkSession.builder.appName("fraud-scala")
      .config("spark.sql.session.timeZone", "UTC")
      .config("spark.sql.shuffle.partitions", "4")
      .getOrCreate()
    import spark.implicits._
    spark.sparkContext.setLogLevel("WARN")

    // skema amplop Debezium (hanya kolom yang dipakai)
    val after = new StructType()
      .add("id_trx", StringType)
      .add("id_rekening", StringType)
      .add("id_perangkat", StringType)
      .add("nominal", LongType)
      .add("waktu", LongType)                 // mikrodetik epoch dari Debezium
    val env = new StructType()
      .add("after", after)
      .add("op", StringType)
      .add("ts_ms", LongType)

    val raw = spark.readStream.format("kafka")
      .option("kafka.bootstrap.servers", broker)
      .option("subscribe", "bank.public.transaksi")
      .option("startingOffsets", "earliest")
      .load()

    val trx = raw
      .select(from_json($"value".cast("string"), env).as("e"))
      .where($"e.op".isin("c", "r"))          // insert dan snapshot awal
      .select("e.after.*", "e.ts_ms")
      .withColumn("event_time", expr("timestamp_micros(waktu)"))

    val peringatan = trx
      .withWatermark("event_time", "2 minutes")
      .groupBy(window($"event_time", "1 minute"), $"id_rekening")
      .agg(count(lit(1)).as("n_trx"), sum("nominal").as("total"),
           approx_count_distinct("id_perangkat").as("n_perangkat"))
      .where($"n_trx" > 5 && $"n_perangkat" > 1)

    val kueri = peringatan
      .select($"id_rekening".as("key"),
              to_json(struct($"window.start".as("window_start"), $"id_rekening",
                             $"n_trx", $"total", $"n_perangkat")).as("value"))
      .writeStream.format("kafka")
      .option("kafka.bootstrap.servers", broker)
      .option("topic", "bank.peringatan")
      .option("checkpointLocation", s"$ckpt/fraud_kafka")
      .outputMode("update")
      .trigger(Trigger.ProcessingTime("5 seconds"))
      .start()

    kueri.awaitTermination()
  }
}
