ThisBuild / scalaVersion := "2.13.16"

lazy val root = (project in file("."))
  .settings(
    name := "total-kanal",
    libraryDependencies += "org.apache.spark" %% "spark-sql" % "4.0.1"
  )
