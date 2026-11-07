// Kode 8.7: laporan harian per cabang dalam Scala.
// sbt package lalu:
// spark-submit --class Harian target/scala-2.12/harian_2.12-0.1.jar data
ThisBuild / scalaVersion := "2.12.18"
name := "harian"
version := "0.1"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.5.1" % "provided"
