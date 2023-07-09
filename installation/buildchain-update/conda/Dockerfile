ARG DOCKERHUB_USER
ARG CUDA_VERSION
ARG UBUNTU_VERSION

FROM ${DOCKERHUB_USER}/cudagl:${CUDA_VERSION}-devel-ubuntu${UBUNTU_VERSION}
MAINTAINER James Shen <jierans@sas.upenn.edu>

ENV DEBIAN_FRONTEND=noninteractive
SHELL ["/bin/bash", "-l", "-c"]
RUN apt update && apt upgrade -y
RUN apt install wget git -y
WORKDIR /opt/
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
RUN chmod +x Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
RUN ./Miniconda3-py310_23.3.1-0-Linux-x86_64.sh -b -p /opt/miniconda3
RUN rm Miniconda3-py310_23.3.1-0-Linux-x86_64.sh
RUN cp /opt/miniconda3/etc/profile.d/conda.sh /etc/profile.d/10-conda.sh
RUN conda create -y --name chroma python=3.10 numpy
COPY 11-conda_activate.sh /etc/profile.d/
RUN conda install -y numpy