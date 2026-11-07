// Menampilkan blok sebuah berkas HDFS dan DataNode yang menyimpannya (Kode 3.x).
// Jalankan: sbt "run hdfs://namenode:8020 /lake/bronze/transaksi/part-0000.parquet"
import java.net.URI
import org.apache.hadoop.conf.Configuration
import org.apache.hadoop.fs.{FileSystem, Path}

object LokasiBlok {
  def main(args: Array[String]): Unit = {
    val Array(uri, berkas) = args
    val fs = FileSystem.get(new URI(uri), new Configuration())
    val st = fs.getFileStatus(new Path(berkas))
    println(s"ukuran ${st.getLen} byte, blok ${st.getBlockSize} byte, replikasi ${st.getReplication}")
    // Satu BlockLocation per blok: offset, panjang, dan host yang memegang replikanya
    for (b <- fs.getFileBlockLocations(st, 0, st.getLen)) {
      println(f"offset ${b.getOffset}%12d  panjang ${b.getLength}%10d  host ${b.getHosts.mkString(", ")}")
    }
    fs.close()
  }
}
