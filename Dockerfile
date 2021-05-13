FROM python:3.9.4-alpine

WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk update \
  && apk add postgresql postgresql-dev gcc python3-dev musl-dev libjpeg jpeg-dev zlib-dev
RUN pip install --upgrade pip

RUN mkdir media
COPY . .
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]