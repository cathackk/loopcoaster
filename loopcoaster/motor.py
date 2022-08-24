from functools import lru_cache
from typing import Union

import buildhat

import testing


AnyMotor = Union[buildhat.Motor, testing.DummyMotor]


@lru_cache()
def get_motor(port: str, dummy: bool = False) -> AnyMotor:
    motor_cls = buildhat.Motor if not dummy else testing.DummyMotor
    return motor_cls(port)
