FROM python:3.9-alpine

COPY Makefile .
COPY requirements.txt .

RUN make install

ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY loops .

CMD ["python3", "/usr/src/app/test.py"]
