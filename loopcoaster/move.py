#!/usr/bin/env python3

import buildhat
import click

import testing


DEFAULT_SPEED = 100.0
DEFAULT_PLIMIT = 1.0
DEFAULT_PORT = 'A'

@click.command()
@click.argument('rotations', type=float, required=True)
@click.argument('speed', type=float, default=DEFAULT_SPEED)
@click.option('--plimit', type=float, default=DEFAULT_PLIMIT)
@click.option('--port', '-p', type=click.Choice('ABCD'), default=DEFAULT_PORT, help='Which buildhat port controls the motor')
@click.option('--dummy/--real', type=bool, default=False, help='Use dummy motor class instead of controlling a real motor')
def _move(*args, **kwargs):
    move(*args, **kwargs)


def move(
    rotations: float,
    speed: float = DEFAULT_SPEED,
    plimit: float = DEFAULT_PLIMIT,
    port: str = DEFAULT_PORT,
    dummy: bool = False
):
    motor_cls = buildhat.Motor if not dummy else testing.DummyMotor
    motor = motor_cls(port)
    motor.plimit(plimit)
    motor.run_for_rotations(rotations=rotations, speed=speed)
    motor.stop()


if __name__ == '__main__':
    _move()
