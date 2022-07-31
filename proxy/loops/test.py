import os
from functools import partial

import pika
import pika.channel

EXCHANGE = 'exchange'
ROUTING_KEY = 'exchange.stuff'


def main():
    amqp_url = os.environ['AMQP_URL']
    print(f'>>> {amqp_url=}')

    params = pika.URLParameters(amqp_url)
    connection = pika.SelectConnection(params, on_open_callback=on_open)

    try:
        connection.ioloop.start()
    except KeyboardInterrupt:
        connection.close()
        connection.ioloop.stop()


def on_open(connection: pika.BaseConnection):
    """callback: connected to the AMQP broker"""
    print('>>> connected')
    connection.channel(on_open_callback=on_channel_open)


def on_channel_open(channel: pika.channel.Channel):
    """callback: opened a channel on the connection"""
    print('>>> channel open')
    channel.exchange_declare(
        exchange=EXCHANGE,
        exchange_type='direct',
        durable=True,
        callback=partial(on_exchange, channel)
    )


def on_exchange(channel: pika.channel.Channel, frame):
    """callback: exchange declared"""
    print(">>> exchange declared")
    send_message(channel, 1)


def send_message(channel: pika.channel.Channel, index: int):
    """Send message to the queue"""
    message = f'message #{index}'
    print(f">>> sending {message!r}")
    channel.basic_publish(
        exchange=EXCHANGE,
        routing_key=ROUTING_KEY,
        body=message.encode(),
        properties=pika.BasicProperties(
            content_type='text/plain',
            delivery_mode=2  # persistent
        )
    )


if __name__ == '__main__':
    main()
