FROM python:3.6-alpine

RUN adduser -D gridfs

WORKDIR /home/gridfs

RUN cd /home/gridfs

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app.py app.py
COPY .env .env
COPY boot.sh boot.sh
RUN chmod +x boot.sh

ENV FLASK_APP app.py

RUN chown -R gridfs:gridfs ./
USER gridfs

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
