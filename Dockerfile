FROM python:3.9-slim as base

# Enables Python tracebacks on segfaults
# and disable pyc files from being written at import time
ENV PYTHONFAULTHANDLER=1 \
    PYTHONBUFFERED=1  \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/project"

RUN apt-get update && apt-get install --no-install-recommends -y \
        # deps for building python deps
        build-essential

WORKDIR /project

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /project/

RUN apt-get purge -y build-essential

CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
