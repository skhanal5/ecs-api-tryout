FROM python:3.12-slim AS builder

RUN pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock ./
RUN pipenv install --deploy --system

FROM python:3.12-slim

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY src/ src/

RUN useradd -m appuser
USER appuser

CMD ["fastapi", "run", "./src/main.py", "--port", "80"]
