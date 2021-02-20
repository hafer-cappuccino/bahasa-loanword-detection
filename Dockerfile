FROM python:3.9-slim as base

ARG POETRY_VERSION

ENV POETRY_VERSION=${POETRY_VERSION:-1.1.4} \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PIP_NO_CACHE_DIR=true \
    AIRFLOW_HOME=$AIRFLOW_HOME \
    # Enables Python tracebacks on segfaults
    # and disable pyc files from being written at import time
    PYTHONFAULTHANDLER=1 \
    PYTHONBUFFERED=1  \
    PYTHONDONTWRITEBYTECODE=1

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        # deps for installing poetry
        curl \
        # deps for building python deps
        build-essential

RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python

WORKDIR /project

COPY poetry.lock pyproject.toml ./

RUN poetry install

COPY . /project/

VOLUME /out

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
