import os

import requests

RABBITMQ_USER = os.environ['RABBITMQ_USER']
RABBITMQ_PASS = os.environ['RABBITMQ_PASS']
RABBITMQ_HOST = os.environ['RABBITMQ_HOST']
RABBITMQ_POST = os.environ['RABBITMQ_PORT']
RABBITMQ_EXCHANGE = os.environ['RABBITMQ_EXCHANGE']
RABBITMQ_QUEUE = os.environ['RABBITMQ_QUEUE']
RABBITMQ_ROUTING_KEY = os.environ['RABBITMQ_ROUTING_KEY']


def send_to_queue(message: bytes) -> bool:
    response = requests.post(
        url=f'http://{RABBITMQ_HOST}:{RABBITMQ_POST}/api/exchanges/%2f/{RABBITMQ_EXCHANGE}/publish',
        auth=(RABBITMQ_USER, RABBITMQ_PASS),
        json={
            'properties': {},
            'routing_key': RABBITMQ_ROUTING_KEY,
            'payload': message.decode(),
            'payload_encoding': 'string',
        },
        headers={
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()
    return response.json()['routed']


def receive_from_queue():
    response = requests.post(
        url=f'http://{RABBITMQ_HOST}:{RABBITMQ_POST}/api/queues/%2f/{RABBITMQ_QUEUE}/get',
        auth=(RABBITMQ_USER, RABBITMQ_PASS),
        json={
            'count': 1,
            'encoding': 'auto',
            'ackmode': 'ack_requeue_false',
        },
        headers={
            'Content-Type': 'application/json'
        }
    )
    response.raise_for_status()

    received_messages = response.json()
    # TODO: also return metadata
    return [message['payload'] for message in received_messages]
