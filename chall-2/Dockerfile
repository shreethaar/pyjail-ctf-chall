FROM python3:10-slim
WORKDIR /app

COPY challenge.py
COPY flag.txt

RUN chmod 400 flag.txt

EXPOSE 1337

CMD["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:/usr/bin/python3 /app/challenge.py"]
