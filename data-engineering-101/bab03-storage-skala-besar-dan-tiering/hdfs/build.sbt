ThisBuild / scalaVersion := "2.13.16"

lazy val root = (project in file("."))
  .settings(
    name := "lokasi-blok-hdfs",
    libraryDependencies += "org.apache.hadoop" % "hadoop-client" % "3.4.1"
  )
