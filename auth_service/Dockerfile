FROM alpine:latest

RUN apk update && \
    apk add --no-cache \
    python3 \
    py3-pip \
    py3-virtualenv

RUN if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi

WORKDIR /app

RUN python3 -m venv .venv

RUN mkdir /app/app
COPY . /app/app

RUN /app/.venv/bin/pip3 install -r /app/app/requirements.txt

CMD [ "/app/.venv/bin/python3", "-m", "app.main" ]
