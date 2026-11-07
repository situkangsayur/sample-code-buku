// Kode 1.3: actor penghitung dengan Apache Pekko (Typed).
// Jalankan: sbt run
ThisBuild / scalaVersion := "3.3.6"

lazy val root = (project in file("."))
  .settings(
    name := "pekko-penghitung",
    libraryDependencies += "org.apache.pekko" %% "pekko-actor-typed" % "1.1.5"
  )
