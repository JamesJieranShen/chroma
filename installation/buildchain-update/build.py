import argparse

import docker
import subprocess
import logging
import os
import sys


def build_cudagl(build_args, push=False):
    userName = build_args['DOCKERHUB_USER']
    cudaVersion = build_args['CUDA_VERSION']
    osVersion = build_args['UBUNTU_VERSION']
    distro = 'ubuntu'
    arch = 'x86_64'
    log = logging.getLogger('CUDAGL_BUILD')
    log.setLevel(logging.INFO)
    cmd = f"./build.sh -d --image-name {userName}/cudagl " \
          f"--cuda-version {cudaVersion} " \
          f"--os {distro} --os-version {osVersion} " \
          f"--arch {arch} --cudagl --push"
    log.warning(f"Beginning Build: {cmd}")
    cwd = os.getcwd()
    log.warning(f"Current Working Directory: {cwd}")
    os.chdir('cudagl')
    log.warning(f"Command: {cmd}")
    os.system(cmd)
    os.chdir(cwd)
    log.warning(f"Current Working Directory: {os.getcwd()}")
    log.warning("Build Complete")
    if push:
        log.warning(f"Pushing all images in repo {userName}/cudagl")
        os.system(f"docker push {userName}/cudagl --all-tags")
        log.warning("Push Complete")


def buildAndStreamLog(path, tag, buildargs, log, pull=True, nocache=False, push=False):
    build_arg_str = ' '.join([f"--build-arg {k}={v}" for k, v in buildargs.items()])
    cmd = f"docker build -t {tag} {build_arg_str}"
    if pull:
        cmd += " --pull"
    if nocache:
        cmd += " --no-cache"
    cmd += f" {path}"
    log.warning(f"Beginning Build: Context: {path}\tTag: {tag}")
    log.warning(f"Command: {cmd}")
    os.system(cmd)
    log.warning("Build Complete")
    if push:
        log.warning(f"Pushing image: {tag}")
        os.system(f"docker push {tag}")
        log.warning("Push Complete")
    # apiClient = docker.APIClient(base_url='unix://var/run/docker.sock')
    # log.warning(f"Context: {path}")
    # log.warning(f"building image: {tag}")
    # streamer = apiClient.build(path=path, tag=tag, pull=pull, buildargs=buildargs, decode=True, nocache=nocache)
    # for chunk in streamer:
    #     if 'stream' in chunk:
    #         log.info(chunk['stream'].strip())
    #     if 'error' in chunk:
    #         log.error(chunk['error'].strip())


def build_conda(build_args, pull=True, nocache=False, push=False):
    log = logging.getLogger('CONDA_BUILD')
    log.setLevel(logging.INFO)
    tag = f"{build_args['DOCKERHUB_USER']}/chroma3:" \
          f"cuda_{build_args['CUDA_VERSION']}__ubuntu_{build_args['UBUNTU_VERSION']}__intermediates_conda"
    buildAndStreamLog('conda', tag, build_args, log, pull, nocache, push)


def build_root(build_args, pull=True, nocache=False, push=False):
    log = logging.getLogger('ROOT_BUILD')
    log.setLevel(logging.INFO)
    tag = f"{build_args['DOCKERHUB_USER']}/chroma3:" \
          f"cuda_{build_args['CUDA_VERSION']}__ubuntu_{build_args['UBUNTU_VERSION']}" \
          f"__intermediates_root_{build_args['ROOT_VERSION']}"
    buildAndStreamLog('root', tag, build_args, log, pull, nocache, push)


def build_g4(build_args, pull=True, nocache=False, push=False):
    log = logging.getLogger('G4_BUILD')
    log.setLevel(logging.INFO)
    tag = f"{build_args['DOCKERHUB_USER']}/chroma3:" \
          f"cuda_{build_args['CUDA_VERSION']}__ubuntu_{build_args['UBUNTU_VERSION']}" \
          f"__intermediates_g4_{build_args['GEANT4_VERSION']}"
    buildAndStreamLog('geant4', tag, build_args, log, pull, nocache, push)


def build_chroma(build_args, pull=True, nocache=False, push=False):
    log = logging.getLogger('CHROMA_BUILD')
    log.setLevel(logging.INFO)
    tag = f"{build_args['DOCKERHUB_USER']}/chroma3:" \
          f"cuda_{build_args['CUDA_VERSION']}__ubuntu_{build_args['UBUNTU_VERSION']}"
    buildAndStreamLog('chroma', tag, build_args, log, pull, nocache, push)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Build docker images for chroma3')
    parser.add_argument('--cudagl', action='store_true', help='Build cudagl image')
    parser.add_argument('--conda', action='store_true', help='Build conda image')
    parser.add_argument('--root', action='store_true', help='Build root image')
    parser.add_argument('--g4', action='store_true', help='Build g4 image')
    parser.add_argument('--chroma', action='store_true', help='Build chroma image')
    parser.add_argument('--all', action='store_true', help='Build all images')

    parser.add_argument('--pull', action='store_true', help='Pull base image before building')
    parser.add_argument('--nocache', action='store_true', help='Do not use cache when building')
    parser.add_argument('--push', action='store_true', help='Push image after building')
    args = parser.parse_args()
    # If all is set, individual image build should not be specified
    assert not (args.all and (args.cudagl or args.conda or args.root or args.g4 or args.chroma))
    # If no images are specified, print help
    if not (args.cudagl or args.conda or args.root or args.g4 or args.chroma or args.all):
        parser.print_help()
        exit(0)
    # If all is set, ignore pull and nocache flags
    if args.all:
        logging.warning("Building all images from scratch, --pull ignored")
    build_args = {
        'DOCKERHUB_USER': 'stjimmys',
        'CUDA_VERSION': '12.2.0',
        'UBUNTU_VERSION': '22.04',
        'ROOT_VERSION': '6.28.04',
        'GEANT4_VERSION': '11.1.2'
    }
    logging.basicConfig()
    if args.cudagl:
        build_cudagl(build_args, push=args.push)
    if args.conda:
        build_conda(build_args, pull=args.pull, nocache=args.nocache, push=args.push)
    if args.root:
        build_root(build_args, pull=args.pull, nocache=args.nocache, push=args.push)
    if args.g4:
        build_g4(build_args, pull=args.pull, nocache=args.nocache, push=args.push)
    if args.chroma:
        build_chroma(build_args, pull=args.pull, nocache=args.nocache, push=args.push)
    if args.all:
        build_cudagl(build_args, push=args.push)
        build_root(build_args, pull=False, nocache=args.nocache, push=args.push)
        build_g4(build_args, pull=False, nocache=args.nocache, push=args.push)
        build_chroma(build_args, pull=False, nocache=args.nocache, push=args.push)