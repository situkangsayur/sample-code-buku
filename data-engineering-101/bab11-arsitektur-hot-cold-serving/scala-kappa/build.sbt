// Kode 11.3: job Kappa versi kedua (replay dari offset awal).
// sbt package lalu:
// spark-submit --class KappaReplay \
//   --packages org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.1,org.apache.iceberg:iceberg-spark-runtime-4.0_2.13:1.10.1 \
//   target/scala-2.13/kappa-replay_2.13-0.1.jar
ThisBuild / scalaVersion := "2.13.16"
name := "kappa-replay"
version := "0.1"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "4.0.1" % "provided"
