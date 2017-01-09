FROM gliderlabs/alpine:latest

COPY requirements.txt run.py /server/

RUN apk --no-cache add \
    python \
    py-pip \
  && apk --update add --virtual build-dependencies gcc python-dev build-base \
  && pip install -r /server/requirements.txt \
  && apk del build-dependencies \
  && adduser -D app \
  && mkdir -p /server  \
  && chown -R app:app /server

COPY app /server/app/

VOLUME /tmp

RUN chown -R app:app /server

WORKDIR /server

USER app

EXPOSE 8080

CMD ["python", "run.py"]
