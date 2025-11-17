FROM alpine:latest

ENV PYTHONUNBUFFERED=1

RUN apk update && apk add --update-cache --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing hping3

# Install hping3 and python3
RUN apk add --no-cache \
    python3 \
    py3-pip \
    && rm -rf /var/cache/apk/*

# Install Python packages
RUN pip3 install --no-cache-dir --break-system-packages colorama

# Set working directory
WORKDIR /app

# Set the default command
CMD ["python3", "/app/hping_script.py"]