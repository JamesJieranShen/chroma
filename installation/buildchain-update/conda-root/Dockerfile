ARG DOCKERHUB_USER
ARG CUDA_VERSION
ARG UBUNTU_VERSION

FROM ${DOCKERHUB_USER}/chroma3:cuda_${CUDA_VERSION}__ubuntu_${UBUNTU_VERSION}__intermediates_conda
ARG ROOT_VERSION
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
RUN wget https://root.cern/download/root_v${ROOT_VERSION}.source.tar.gz
RUN tar -xzf root_v${ROOT_VERSION}.source.tar.gz
RUN rm root_v${ROOT_VERSION}.source.tar.gz
WORKDIR /opt/root-${ROOT_VERSION}/build-root
RUN cmake -DCMAKE_INSTALL_PREFIX=/opt/root \
    -Ddavix=OFF \
    -Dwebgui=OFF -Droot7=OFF \
    -DPython3_EXECUTABLE=/opt/miniconda3/envs/chroma/bin/python \
    /opt/root-${ROOT_VERSION}
RUN make -j$(nproc) && make install
RUN rm -rf /opt/root-${ROOT_VERSION}
COPY 20-setup_root.sh /etc/profile.d/

