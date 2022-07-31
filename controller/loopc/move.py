#!/usr/bin/env python3

import buildhat
import click

import testing


@click.command()
@click.argument('rotations', type=float, required=True)
@click.argument('speed', type=float, default=100.0)
@click.option('--plimit', type=float, default=1.0)
@click.option('--port', '-p', type=click.Choice('ABCD'), default='A', help='Which buildhat port controls the motor')
@click.option('--dummy/--real', type=bool, default=False, help='Use dummy motor class instead of controlling a real motor')
def move(rotations: float, speed: float, plimit: float, port: str, dummy: bool):
    motor_cls = buildhat.Motor if not dummy else testing.DummyMotor
    motor = motor_cls(port)
    motor.plimit(plimit)
    motor.run_for_rotations(rotations=rotations, speed=speed)
    motor.stop()


if __name__ == '__main__':
    move()
