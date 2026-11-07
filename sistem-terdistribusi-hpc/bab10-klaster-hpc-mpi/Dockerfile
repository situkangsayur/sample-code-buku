# Kode 10.18: lingkungan Open MPI + mpi4py untuk praktikum.
#   docker build -t mpi-lab .
#   docker run --rm -it -v "$PWD":/kerja -w /kerja mpi-lab bash
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential openmpi-bin libopenmpi-dev python3-mpi4py python3-numpy \
    && rm -rf /var/lib/apt/lists/*
ENV OMPI_ALLOW_RUN_AS_ROOT=1 OMPI_ALLOW_RUN_AS_ROOT_CONFIRM=1
WORKDIR /kerja
