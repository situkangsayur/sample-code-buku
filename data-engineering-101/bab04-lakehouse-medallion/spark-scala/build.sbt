// Kode 4.23: proyek Scala untuk SilverMerge (Spark 4.0 + Iceberg 1.10).
ThisBuild / scalaVersion := "2.13.16"

lazy val root = (project in file("."))
  .settings(
    name := "bab04-silver-merge",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "4.0.1" % "provided",
      "org.apache.iceberg" % "iceberg-spark-runtime-4.0_2.13" % "1.10.0"
    )
  )
