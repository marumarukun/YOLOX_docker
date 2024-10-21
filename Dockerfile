FROM nvidia/cuda:12.4.1-devel-ubuntu22.04

ENV TZ=Asia/Tokyo
ENV PIP_DEFAULT_TIMEOUT=100000
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && \
    apt-get install -y \
    git \
    python3 \
    python3-pip \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/bin/python3 /usr/bin/python

WORKDIR /workspace

# 依存関係をインストール
COPY requirements.txt setup.py README.md ./
COPY yolox ./yolox
COPY tools ./tools
COPY exps ./exps
RUN pip3 install -U pip && \
    pip3 install -r requirements.txt && \
    pip3 install -v -e . && \
    pip3 install cython && \
    pip3 install 'git+https://github.com/cocodataset/cocoapi.git#subdirectory=PythonAPI'

# Pythonのパスを設定
ENV PYTHONPATH="/workspace:${PYTHONPATH}"
