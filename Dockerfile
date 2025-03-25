FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# standart package builds
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

#pipx for poetry
RUN python3 -m pip install --user pipx

ENV PATH="/root/.local/bin:${PATH}"

RUN python3 -m pipx ensurepath

RUN pipx install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock /app/

RUN poetry install --no-root

COPY . /app/

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

EXPOSE 8000
# For remote debugging
EXPOSE 5678
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD curl -f http://localhost:8000/api/status || exit 1
# Set the entrypoint
CMD ["/app/entrypoint.sh"]

