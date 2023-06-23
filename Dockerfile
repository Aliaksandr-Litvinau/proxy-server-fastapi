FROM python:3.9-slim-buster

WORKDIR /app

COPY ./ .

RUN pip install --no-cache-dir -r requirements.txt

RUN set -o allexport; \
    [ -f .env.example ] && . .env.example; \
    set +o allexport

ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
