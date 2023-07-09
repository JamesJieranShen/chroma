ARG DOCKERHUB_USER
ARG CUDA_VERSION
ARG UBUNTU_VERSION

FROM ${DOCKERHUB_USER}/chroma3:cuda_${CUDA_VERSION}__ubuntu_${UBUNTU_VERSION}__intermediates_conda
ARG GEANT4_VERSION
MAINTAINER James Shen <jierans@sas.upenn.edu>

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-l", "-c"]
RUN apt update && apt install  -y \
    dpkg-dev \
    cmake \
    g++ \
    gcc \
    binutils \
    libx11-dev \
    libxpm-dev \
    libxft-dev \
    libxext-dev \
    libpng-dev \
    libjpeg-dev \
    libgsl-dev \
    libfftw3-dev \
    libpcre3-dev \
    libxml2-dev \
    libssl-dev
RUN apt install -y libxerces-c-dev libxmu-dev libxi-dev freeglut3-dev

WORKDIR /opt/
RUN git clone https://gitlab.cern.ch/geant4/geant4.git --depth 1 --branch v${GEANT4_VERSION} geant4-${GEANT4_VERSION}
WORKDIR /opt/geant4-${GEANT4_VERSION}/build-geant4
RUN cmake -DGEANT4_INSTALL_DATA=ON \
    -DCMAKE_INSTALL_PREFIX=/opt/geant4  \
    -DGEANT4_USE_GDML=ON  \
    -DGEANT4_USE_OPENGL_X11=ON  \
    -DGEANT4_USE_XM=OFF  \
    -DGEANT4_BUILD_TLS_MODEL=global-dynamic \
    /opt/geant4-${GEANT4_VERSION}
RUN make -j$(nproc) && make install
COPY 30-setup_geant4.sh /etc/profile.d/
WORKDIR /opt
RUN rm -rf /opt/geant4-${GEANT4_VERSION}
RUN pip install geant4-pybind


