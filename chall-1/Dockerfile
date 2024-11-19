FROM python:3.11-slim
WORKDIR /app
COPY app.py /app/app.py

RUN useradd -m ctfuser

RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
USER ctfuser
EXPOSE 1337

CMD ["python3","/app/app.py"]

