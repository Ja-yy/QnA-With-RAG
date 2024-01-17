FROM ghcr.io/chroma-core/chroma:latest

RUN apt-get update \
    && apt-get install -y build-essential libomp-dev

RUN pip install --force-reinstall --no-cache-dir hnswlib