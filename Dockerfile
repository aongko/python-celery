FROM python:3.7-slim-buster as base

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y apt-utils \
    && apt-get install -y build-essential \
    && apt-get purge -y --auto-remove \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -U pip pipenv \
    && groupadd -r mygroup && useradd -rm -g mygroup myuser

USER myuser

COPY Pipfile Pipfile.lock ./

RUN PIP_USER=1 pipenv install --system --ignore-pipfile --deploy


FROM python:3.7-slim-buster

RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -U pip pipenv \
    && groupadd -r mygroup && useradd -rm -g mygroup myuser \
    && mkdir -p /home/myuser/app \
    && chown -R myuser:mygroup /home/myuser/app

USER myuser

COPY --from=base --chown=myuser:mygroup /home/myuser/.local /home/myuser/.local
ENV PATH=$PATH:/home/myuser/.local/bin

WORKDIR /home/myuser/app

COPY --chown=myuser:mygroup . .
