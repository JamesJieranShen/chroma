FROM nvidia/cudagl:11.3.0-devel
MAINTAINER James Shen <jierans@sas.upenn.edu>

USER root
SHELL ["/bin/bash", "-l", "-c"] 
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get upgrade -y
RUN apt-get update && apt-get install -y vim curl git wget python3 python3-pip python3-venv

CMD ["/bin/bash","-l"]
