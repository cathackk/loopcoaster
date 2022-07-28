#!/usr/bin/env python3

from buildhat import Motor
import click


@click.command()
@click.argument('rotations', type=float, required=True)
@click.argument('speed', type=float, default=100.0)
@click.option('--plimit', type=float, default=1.0)
@click.option('--port', '-p', type=click.Choice('ABCD'), default='A', help='Which buildhat port controls the motor')
def move(rotations: float, speed: float, plimit: float, port: str):
    motor = Motor(port)
    motor.plimit(plimit)
    motor.run_for_rotations(rotations=rotations, speed=speed)


if __name__ == '__main__':
    move()
