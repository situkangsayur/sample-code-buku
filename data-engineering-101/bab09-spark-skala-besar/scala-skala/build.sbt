// Kode 9.5: salting dalam Scala.
// sbt package lalu: spark-submit --class Salting target/scala-2.12/skala_2.12-0.1.jar 5000000
ThisBuild / scalaVersion := "2.12.18"
name := "skala"
version := "0.1"
libraryDependencies += "org.apache.spark" %% "spark-sql" % "3.5.1" % "provided"
