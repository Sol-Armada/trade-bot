FROM python:bullseye

WORKDIR /src

COPY . ./

RUN useradd developer && chown -R developer /src


