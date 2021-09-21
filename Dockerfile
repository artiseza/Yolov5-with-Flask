FROM ubuntu:18.04
RUN apt-get update && apt-get install -y --no-install-recommends \
        wget \
        git \
        vim \
        curl \
        python3 \
        python3-dev \
        python3-pip \
        python3-setuptools \
        rsync \
        software-properties-common \
        sudo \
        sqlite3 \
        zip \
        unzip \
        rar \
        unrar \
        apache2-utils
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip3 --no-cache-dir install --upgrade pip
RUN pip3 --no-cache-dir install \
        numpy==1.19.5 \
        scipy==1.5.4 \
        flask==1.1.2 \
        pandas==1.1.5 \
        sklearn \
        requests==2.25.1 \
        pyyaml==5.4.1 \
        cryptography==3.4.6 \
        flask-htpasswd==0.4.0
ENTRYPOINT bash
