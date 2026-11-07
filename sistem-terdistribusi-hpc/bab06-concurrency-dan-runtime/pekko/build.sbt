// Proyek Java dengan Apache Pekko (actor bertipe). Jalankan: sbt run
ThisBuild / scalaVersion := "2.13.15"   // Pekko butuh pustaka Scala; kode kita Java
ThisBuild / organization := "contoh"

lazy val root = (project in file("."))
  .settings(
    name := "bab06-pekko",
    javacOptions ++= Seq("--release", "21"),
    libraryDependencies ++= Seq(
      "org.apache.pekko" %% "pekko-actor-typed" % "1.1.3",
      "ch.qos.logback"    % "logback-classic"   % "1.5.12"
    ),
    run / fork := true
  )
