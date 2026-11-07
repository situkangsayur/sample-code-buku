// Contoh Apache Pekko Cluster Sharding (Scala). Jalankan: lihat README.md
ThisBuild / scalaVersion := "2.13.15"

val pekkoVersion = "1.1.3"

lazy val root = (project in file("."))
  .settings(
    name := "pekko-sharding",
    libraryDependencies ++= Seq(
      "org.apache.pekko" %% "pekko-actor-typed"             % pekkoVersion,
      "org.apache.pekko" %% "pekko-cluster-sharding-typed"  % pekkoVersion,
      "org.apache.pekko" %% "pekko-serialization-jackson"   % pekkoVersion,
      "ch.qos.logback"    % "logback-classic"               % "1.5.12"
    ),
    run / fork := true
  )
