# A small, non-root image. Replace the build and run steps with your application's.
#
#   docker build -t my-image .
#   docker run --rm my-image

ARG PYTHON_VERSION=3.15

# --- build: install dependencies into a virtual environment ------------------------------------
FROM python:${PYTHON_VERSION}-slim AS build

ENV PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /src
RUN python -m venv /opt/venv

# To install dependencies, add a requirements.txt, allow it in Dockerfile.dockerignore and
# uncomment these two lines. Copying it before the application keeps the install layer cached
# until the requirements change.
#
# COPY requirements.txt ./
# RUN /opt/venv/bin/pip install -r requirements.txt

COPY app ./app

# --- run: the same base without build tools or sources -----------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ARG VERSION=0.0.0
LABEL org.opencontainers.image.title="docker-public-repo-template" \
      org.opencontainers.image.description="Replace with a description of your image" \
      org.opencontainers.image.source="https://github.com/OWNER/REPOSITORY" \
      org.opencontainers.image.licenses="MIT" \
      org.opencontainers.image.version="${VERSION}"

RUN useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app
COPY --from=build /opt/venv /opt/venv
COPY --from=build /src/app /app

ENV PATH="/opt/venv/bin:${PATH}" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

USER 10001
WORKDIR /app
ENTRYPOINT ["python", "main.py"]
