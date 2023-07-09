ARG DOCKERHUB_USER
ARG CUDA_VERSION
ARG UBUNTU_VERSION
ARG GEANT4_VERSION
ARG ROOT_VERSION

FROM ${DOCKERHUB_USER}/chroma3:cuda_${CUDA_VERSION}__ubuntu_${UBUNTU_VERSION}__intermediates_g4_${GEANT4_VERSION} as g4-build
FROM ${DOCKERHUB_USER}/chroma3:cuda_${CUDA_VERSION}__ubuntu_${UBUNTU_VERSION}__intermediates_root_${ROOT_VERSION} as root-build
FROM ${DOCKERHUB_USER}/cudagl:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
ARG GEANT4_VERSION
MAINTAINER James Shen <jierans@sas.upenn.edu>

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-l", "-c"]
RUN apt update && apt upgrade -y && apt install -y wget git cmake python3 python-is-python3 python3-dev python3-pip \
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
    libssl-dev \
    libxerces-c-dev \
    libxmu-dev  \
    libxi-dev  \
    freeglut3-dev
RUN pip install numpy
WORKDIR /opt/

# Copy over G4 and ROOT
COPY --from=g4-build /opt/geant4 /opt/geant4
COPY --from=root-build /opt/root /opt/root
COPY --from=root-build /etc/profile.d/* /etc/profile.d/
COPY --from=g4-build /etc/profile.d/* /etc/profile.d/
CMD ["/bin/bash","-l"]
