#!/usr/bin/env python3

import os.path
import time

import buildhat
import click
import pygame

import testing

LOOP_WAV = 'roller-loop.mp3'
SCREAMS_WAV = 'roller-screams.mp3'


@click.command()
@click.option('--repeats', '-n', type=int, default=1, help='Number of consecutive rides')
@click.option('--wait-seconds', '-w', type=float, default=0.0, help='Wait time between consecutive rides')
@click.option('--raise-speed', '-v1', type=float, default=10.0, help='Speed for the 1st stage "raise"')
@click.option('--raise-rotations', '-r1', type=float, default=28.0, help='Length of the 1st stage "raise"')
@click.option('--kick-speed', '-v2', type=float, default=100.0, help='Speed for the 2nd stage "kick"')
@click.option('--kick-rotations', '-r2', type=float, default=10.0, help='Length of the 2nd stage "kick"')
@click.option('--return-speed', '-v3', type=float, default=80.0, help='Speed for the 3rd stage "return"')
@click.option('--return-rotations', '-r3', type=float, default=25.5, help='Length of the 3rd stage "return"')
@click.option('--sound/--silent', type=bool, default=True, help='Play some nice sounds')
@click.option('--port', '-p', type=click.Choice('ABCD'), default='A', help='Which buildhat port controls the motor')
@click.option('--dummy/--real', type=bool, default=False, help='Use dummy motor class instead of controlling a real motor')
def ride(
    repeats: int,
    wait_seconds: float,
    raise_speed: float,
    raise_rotations: float,
    kick_speed: float,
    kick_rotations: float,
    return_speed: float,
    return_rotations: float,
    sound: bool,
    port: str,
    dummy: bool,
):
    motor_cls = buildhat.Motor if not dummy else testing.DummyMotor

    # motor controlling the elevator
    motor = motor_cls(port)
    motor.plimit(1.0)

    for repeat in range(repeats):
        print(f"ride {repeat + 1}/{repeats} ...")
        if repeat > 0:
            time.sleep(wait_seconds)

        # stage 1: raise
        # - the cart is in the elevator
        # - the elevator is just about to be lifted
        if raise_rotations > 0:
            if sound:
                play_sound(LOOP_WAV, looped=True)
            motor.run_for_rotations(rotations=raise_rotations, speed=raise_speed)

        # stage 2: kick
        # - the elevator is just before the summit
        # - make a fast strong "kick" to push the cart onto the rails
        if kick_rotations > 0:
            if sound:
                play_sound(SCREAMS_WAV)
            motor.run_for_rotations(rotations=kick_rotations, speed=kick_speed)

        # stage 3: return
        # - the cart is on the way down
        # - the elevator is returning to its base position
        if return_rotations > 0:
            motor.run_for_rotations(rotations=return_rotations, speed=return_speed)

    motor.stop()


def play_sound(filename: str, looped: bool = False) -> None:
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    pygame.mixer.music.load(resource_path(filename))
    pygame.mixer.music.play(loops=-1 if looped else 1)


def resource_path(filename: str) -> str:
    loopcoaster_dir = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(loopcoaster_dir, 'resources', filename)


if __name__ == '__main__':
    ride()
