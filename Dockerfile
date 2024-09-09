ARG PYTHON_VERSION=3.11.9

FROM python:${PYTHON_VERSION}-slim-bullseye AS builder

# --- Install Poetry ---
ARG POETRY_VERSION=1.8.3

ENV POETRY_HOME=/opt/poetry
ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1
ENV POETRY_VIRTUALENVS_CREATE=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Tell Poetry where to place its cache and virtual environment
ENV POETRY_CACHE_DIR=/opt/.cache

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==${POETRY_VERSION}" &&  \
    poetry install --no-root --without dev &&  \
    rm -rf $POETRY_CACHE_DIR

FROM python:${PYTHON_VERSION}-slim-bullseye AS dev

ENV VIRTUAL_ENV=/app/.venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY tbot tbot

CMD ["python", "-m", "tbot"]