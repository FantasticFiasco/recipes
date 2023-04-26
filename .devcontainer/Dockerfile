FROM mcr.microsoft.com/vscode/devcontainers/jekyll:1-bullseye

ARG NODE_VERSION="lts/*"
RUN su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"

RUN export DEBIAN_FRONTEND=noninteractive && apt-get update && apt-get upgrade -y
