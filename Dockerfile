FROM python:3.8-alpine

LABEL maintainer = "Felix Fennell <felnne@bas.ac.uk>"

# Setup project
ENV APPPATH /usr/src/app/
ENV PYTHONPATH $APPPATH
ENV FLASK_APP app.py
ENV FLASK_ENV development

WORKDIR $APPPATH

RUN apk add --no-cache libffi-dev libressl-dev build-base git && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir poetry==1.0.0

COPY pyproject.toml poetry.toml poetry.lock $APPPATH
RUN poetry update --no-interaction --no-ansi
RUN poetry install --no-root --no-interaction --no-ansi

# Setup runtime
ENTRYPOINT []
