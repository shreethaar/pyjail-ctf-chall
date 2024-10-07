# Dockerfile
FROM python:3.9-slim

# Install required packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    socat \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m -s /bin/bash ctf

# Copy challenge files
WORKDIR /home/ctf
COPY pyjail.py .
COPY flag.txt .

# Set permissions
RUN chown -R root:root /home/ctf && \
    chmod 555 /home/ctf/pyjail.py && \
    chmod 444 /home/ctf/flag.txt

# Switch to non-root user
USER ctf

# Start socat to handle connections
CMD socat TCP-LISTEN:1337,reuseaddr,fork EXEC:./pyjail.py,pty,stderr
