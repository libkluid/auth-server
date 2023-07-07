FROM python:3.11-alpine

RUN apk update && \
    apk add --no-cache \
        # poetry depends on gcc, python3-dev, libc-dev, libffi-dev
        gcc python3-dev libc-dev libffi-dev && \
    apk add --no-cache \
        # prisma depends on nodejs
        nodejs npm \
        poetry just

WORKDIR /app
ADD ./ ./

RUN poetry install && \
    poetry run prisma generate
CMD just serve
