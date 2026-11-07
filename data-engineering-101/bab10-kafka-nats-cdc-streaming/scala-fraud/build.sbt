// Kode 10.10: aturan fraud dalam Scala (Spark Structured Streaming + sink Kafka).
// sbt package lalu:
// spark-submit --class FraudStream \
//   --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.4 \
//   target/scala-2.12/fraud-scala_2.12-0.1.jar localhost:19092 s3a://lake/ckpt
ThisBuild / scalaVersion := "2.12.18"
name := "fraud-scala"
version := "0.1"
libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-sql"            % "3.5.1" % "provided",
  "org.apache.spark" %% "spark-sql-kafka-0-10" % "3.5.1" % "provided"
)
