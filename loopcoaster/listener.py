#!/usr/bin/env python3

from datetime import datetime

import click
import requests
import time

from move import move
from ride import ride


@click.command()
@click.argument('receive_url', type=str, required=True)
@click.option('--user', '-u', type=str)
@click.option('--password', '-p', type=str)
@click.option('--wait-seconds', '-t', type=float, default=5.0)
@click.option('--buffer-size', '-b', type=int, default=1)
def listen(receive_url: str, user: str, password: str, wait_seconds: float, buffer_size: int):
    while True:
        now = datetime.now()

        response = requests.post(
            url=receive_url,
            auth=(user, password),
            headers={'Content-Type': 'application/json'},
            json={'count': buffer_size},
        )

        response_json = response.json()
        received = response_json['received']
        remaining = response_json['remaining']

        print(f'{now:%Y-%m-%dT%H:%M:%S}: received {len(received)} messages, still remaining {remaining}')

        for index, obj in enumerate(received, 1):
            message = obj['message']
            sender = obj['sender']
            ts = datetime.fromtimestamp(obj['ts'])
            print(f'- [{index}/{len(received)}] {sender}@{ts:%Y-%m-%dT%H:%M:%S}: {message}')

            command = message.pop('command')
            if command == 'move':
                move(**message)
            elif command == 'ride':
                ride(**message)
            else:
                print(f'unknown command {command!r}')

        if not remaining:
            time.sleep(wait_seconds)


if __name__ == '__main__':
    listen()
