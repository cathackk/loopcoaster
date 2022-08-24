#!/usr/bin/env python3

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

import os.path
import time

import click
import pygame

from motor import get_motor


# original chain length was 255 -> requires 63.75 rotations
# if the chain gets shorter, the number of required rotations must be changed accordingly
DEFAULT_CHAIN_LENGTH = 255
CHAIN_PIECES_REMOVED = 4
CHAIN_LENGTH = DEFAULT_CHAIN_LENGTH - CHAIN_PIECES_REMOVED
FULL_CYCLE_ROTS = CHAIN_LENGTH * 0.25

DEFAULT_RAISE_ROTS = 28.0
DEFAULT_KICK_ROTS = 10.0
DEFAULT_RETURN_ROTS = FULL_CYCLE_ROTS - DEFAULT_RAISE_ROTS - DEFAULT_KICK_ROTS

DEFAULT_RAISE_SPEED = 50.0
DEFAULT_KICK_SPEED = 100.0
DEFAULT_RETURN_SPEED = 80.0

DEFAULT_REPEATS = 1
DEFAULT_WAIT_SECONDS = 0.0

DEFAULT_PORT = 'A'

LOOP_WAV = 'roller-loop.mp3'
SCREAMS_WAV = 'roller-screams.mp3'
DEFAULT_SOUND_ON = False


@click.command()
@click.option('--repeats', '-n', type=int, default=DEFAULT_REPEATS, help='Number of consecutive rides')
@click.option('--wait-seconds', '-w', type=float, default=DEFAULT_WAIT_SECONDS, help='Wait time between consecutive rides')
@click.option('--raise-speed', '-v1', type=float, default=DEFAULT_RAISE_SPEED, help='Speed for the 1st stage "raise"')
@click.option('--raise-rotations', '-r1', type=float, default=DEFAULT_RAISE_ROTS, help='Length of the 1st stage "raise"')
@click.option('--kick-speed', '-v2', type=float, default=DEFAULT_KICK_SPEED, help='Speed for the 2nd stage "kick"')
@click.option('--kick-rotations', '-r2', type=float, default=DEFAULT_KICK_ROTS, help='Length of the 2nd stage "kick"')
@click.option('--return-speed', '-v3', type=float, default=DEFAULT_RETURN_SPEED, help='Speed for the 3rd stage "return"')
@click.option('--return-rotations', '-r3', type=float, default=DEFAULT_RETURN_ROTS, help='Length of the 3rd stage "return"')
@click.option('--sound/--silent', type=bool, default=DEFAULT_SOUND_ON, help='Play some nice sounds')
@click.option('--port', '-p', type=click.Choice('ABCD'), default=DEFAULT_PORT, help='Which buildhat port controls the motor')
@click.option('--dummy/--real', type=bool, default=False, help='Use dummy motor class instead of controlling a real motor')
def _ride(*args, **kwargs):
    ride(*args, **kwargs)


def ride(
    repeats: int = DEFAULT_REPEATS,
    wait_seconds: float = DEFAULT_WAIT_SECONDS,
    raise_speed: float = DEFAULT_RAISE_SPEED,
    raise_rotations: float = DEFAULT_RAISE_ROTS,
    kick_speed: float = DEFAULT_KICK_SPEED,
    kick_rotations: float = DEFAULT_KICK_ROTS,
    return_speed: float = DEFAULT_RETURN_SPEED,
    return_rotations: float = DEFAULT_RETURN_ROTS,
    sound: bool = DEFAULT_SOUND_ON,
    port: str = DEFAULT_PORT,
    dummy: bool = False,
):
    # motor controlling the elevator
    motor = get_motor(port, dummy)
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
    _ride()
