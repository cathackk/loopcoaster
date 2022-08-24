#!/usr/bin/env python3
import sys
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
    waiting_since = datetime.now()

    while True:
        now = datetime.now()

        response = requests.post(
            url=receive_url,
            auth=(user, password),
            headers={'Content-Type': 'application/json'},
            json={'count': buffer_size},
        )
        if not response.ok:
            log(f'failed to fetch from {receive_url}, check your credentials')
            sys.exit(1)

        response_json = response.json()
        received = response_json['received']
        remaining = response_json['remaining']

        if received:
            log(
                f'\n{now:%Y-%m-%dT%H:%M:%S}: '
                f'received {len(received)} messages after {now - waiting_since}, '
                f'still remaining {remaining}'
            )

            for index, obj in enumerate(received, 1):
                message = obj['message']
                sender = obj['sender']
                ts = datetime.fromtimestamp(obj['ts'])
                log(f'- [{index}/{len(received)}] {sender}@{ts:%Y-%m-%dT%H:%M:%S}: {message}')

                command = message.pop('command')

                try:
                    if command == 'move':
                        move(**message)
                    elif command == 'ride':
                        ride(**message)
                    else:
                        log(f'unknown command {command!r}')

                except TypeError:
                    kwargs_str = ', '.join(f'{key}={value!r}' for key, value in message.items())
                    log(f'failed to execute {command}({kwargs_str})')

            waiting_since = datetime.now()

        else:
            log('.', end='', flush=True)
            time.sleep(wait_seconds)


# TODO: proper logging with logger
def log(*args, **kwargs):
    print(*args, **kwargs, file=sys.stderr)


if __name__ == '__main__':
    listen()
