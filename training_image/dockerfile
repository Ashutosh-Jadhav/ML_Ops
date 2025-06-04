FROM jupyter/base-notebook

USER root 

RUN apt-get update && apt-get install -y git-lfs && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install datasets evaluate transformers[sentencepiece] accelerate nbconvert peft

USER jovyan 

COPY qa.ipynb /home/jovyan/work

CMD ["jupyter", "nbconvert", "--execute", "--to", "notebook", "--inplace", "/home/jovyan/work/qa.ipynb"]
