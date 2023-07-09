FROM nvidia/cudagl:11.3.0-devel-ubuntu20.04 AS build-root
MAINTAINER James Shen <jamesjieranshen@gmail.com>

USER root
COPY chroma_env.sh /etc/profile.d/
SHELL ["/bin/bash", "-l", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y curl git cmake python3 python-is-python3 python3-dev python3-pip
RUN apt-get update && apt-get install -y dpkg-dev  \
    gcc  \
    g++  \
    binutils  \
    libx11-dev  \
    libxpm-dev  \
    libxft-dev  \
    libxext-dev  \
    libgsl-dev  \
    libfftw3-dev  \
    libpcre3-dev \
    libssl-dev \
    libxerces-c-dev \
    libxmu-dev \
    libxi-dev \
    freeglut3-dev
RUN pip install boost numpy

WORKDIR /opt/
RUN curl -O https://root.cern/download/root_v6.22.02.source.tar.gz
RUN tar xf root_v6.22.02.source.tar.gz
RUN rm root_v6.22.02.source.tar.gz
WORKDIR /opt/root-6.22.02/build-root
RUN cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/root  \
    -Dpython3=ON -Ddavix=OFF -Dminuit2=ON -Droofit=ON /opt/root-6.22.02
RUN make -j$(nproc)
RUN make install
WORKDIR /opt
RUN rm -rf /opt/root-6.22.02

FROM nvidia/cudagl:11.3.0-devel-ubuntu20.04 AS build-geant4
MAINTAINER James Shen <jamesjieranshen@gmail.com>

USER root
COPY chroma_env.sh /etc/profile.d/
SHELL ["/bin/bash", "-l", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y curl git cmake python3 python-is-python3 python3-dev python3-pip
RUN apt-get update && apt-get install -y dpkg-dev  \
    gcc  \
    g++  \
    binutils  \
    libx11-dev  \
    libxpm-dev  \
    libxft-dev  \
    libxext-dev  \
    libgsl-dev  \
    libfftw3-dev  \
    libpcre3-dev \
    libssl-dev \
    libxerces-c-dev \
    libxmu-dev \
    libxi-dev \
    freeglut3-dev
RUN pip install boost numpy
COPY --from=build-root /opt/root /opt/root

WORKDIR /opt/
RUN curl -O https://geant4-data.web.cern.ch/geant4-data/releases/geant4.10.05.p01.tar.gz
RUN tar xf geant4.10.05.p01.tar.gz
RUN rm geant4.10.05.p01.tar.gz
WORKDIR /opt/geant4.10.05.p01/build-g4
RUN cmake -DCMAKE_BUILD_TYPE=Release -DGEANT4_INSTALL_DATA=ON -DCMAKE_INSTALL_PREFIX=/opt/geant4 -DGEANT4_USE_GDML=ON -DGEANT4_USE_OPENGL_X11=ON -DGEANT4_USE_XM=OFF /opt/geant4.10.05.p01
RUN make -j$(nproc)
RUN make install
WORKDIR /opt/geant4.10.05.p01
COPY g4py.4.10.05.p01.patch ./
RUN git apply g4py.4.10.05.p01.patch
WORKDIR /opt/geant4.10.05.p01/build-g4py
ARG GEANT4_INSTALL=/opt/geant4
RUN cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX=/opt/geant4  \
    /opt/geant4.10.05.p01/environments/g4py
RUN make -j$(nproc)
RUN sed -i 's/install: preinstall/install:/' Makefile
RUN find . -name '*.cmake' -exec sed -i -n -E '/\.pyc|\.pyo/!p' {} \;
RUN sed -i -E 's/(.*G4LossTableManager.Instance.*)/#\1/' source/python3/__init__.py
RUN make install
WORKDIR /opt
RUN rm -rf /opt/geant4.10.05.p01


FROM nvidia/cudagl:11.3.0-devel-ubuntu20.04
MAINTAINER James Shen <jamesjieranshen@gmail.com>

USER root
COPY chroma_env.sh /etc/profile.d/
SHELL ["/bin/bash", "-l", "-c"]
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y curl git cmake python3 python-is-python3 python3-dev python3-pip
RUN apt-get update && apt-get install -y dpkg-dev  \
    gcc  \
    g++  \
    binutils  \
    libx11-dev  \
    libxpm-dev  \
    libxft-dev  \
    libxext-dev  \
    libgsl-dev  \
    libfftw3-dev  \
    libpcre3-dev \
    libssl-dev \
    libxerces-c-dev \
    libxmu-dev \
    libxi-dev \
    freeglut3-dev
RUN pip install boost numpy
COPY --from=build-root /opt/root /opt/root
COPY --from=build-geant4 /opt/geant4 /opt/geant4
RUN apt-get update && apt-get install -y libgmp-dev libmpfr-dev libgmpxx4ldbl zip unzip patchelf
RUN git clone --branch v0.3 https://github.com/PyMesh/PyMesh.git && \
    cd PyMesh && \
    git submodule update --init && \
    python setup.py build && \
    python setup.py install && \
    cd ..

CMD ["/bin/bash","-l"]
