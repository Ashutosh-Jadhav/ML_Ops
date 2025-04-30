FROM jupyter/base-notebook

ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt-get update && apt-get install -y git-lfs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install datasets evaluate transformers[sentencepiece] accelerate nbconvert

COPY qa.ipynb /home/jovyan/work