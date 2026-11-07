// Total nominal per kanal dengan Spark (Kode 1.4, versi Scala).
// Jalankan: sbt run  (memerlukan JDK 17 atau 21)
import org.apache.spark.sql.SparkSession
import org.apache.spark.sql.functions._

object TotalKanal {
  def main(args: Array[String]): Unit = {
    val spark = SparkSession.builder()
      .appName("total-kanal")
      .master("local[*]")          // satu mesin, semua core
      .getOrCreate()

    val trx = spark.read.parquet("../../lake/silver/transaksi.parquet")
    trx.groupBy("kanal")
      .agg(sum("nominal").as("total"), count(lit(1)).as("jml"))
      .orderBy(desc("total"))
      .show()

    spark.stop()
  }
}
