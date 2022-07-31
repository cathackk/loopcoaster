FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
COPY Makefile .
COPY requirements.txt .
RUN make install

COPY wait-for-it.sh .
COPY init-rabbitmq.sh .
COPY ./app .


CMD ./init-rabbitmq.sh && /start.sh
