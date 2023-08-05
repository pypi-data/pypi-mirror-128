import math
from collections import namedtuple
from enum import Enum

__author__ = "BridgeTechIL"

from typing import Dict


class State(Enum):
    """Elevator status."""

    UP = 1
    DOWN = 2
    IDLE = 3
    VIP = 4


def can_switch(switch_data: Dict, floors_count: int):
    """
    Exception logic for the elevators
    Upon elevation, elevator can perform a switch to a new target, if several conditions are met.

    :param switch_data: Contains elevators current floor, state,
            switch count, switch range, calls queue, target.
    :param floors_count: amount of floor on the site
    :return: Boolean value that determine whether the elevator can perform a switch
    """
    data = namedtuple("elevator", switch_data.keys())(*switch_data.values())
    floor = switch_data.get('floor')
    abs_floor = abs(floor)

    current_target = abs(data.target) if isinstance(data.target, int) else math.inf
    if math.inf == data.current_floor:
        state = 'IDLE'
    state = 'DOWN' if abs(data.current_floor) > abs(current_target) else 'UP'

    left_limit = int(abs(data.current_floor) - data.switch_range if
                     abs(data.current_floor) - data.switch_range > 0 else 0)
    right_limit = int(data.current_floor + data.switch_range if
                      data.current_floor + data.switch_range <= int(floors_count) else int(floors_count))

    def _has_same_direction() -> bool:
        if state == 'DOWN':
            current_target_sign = -1
        elif state == 'UP':
            current_target_sign = 1
        else:
            return False

        return True if abs(floor + current_target_sign) == abs(current_target_sign) + abs(floor) else False

    def _is_new_call() -> bool:
        return True if floor not in data.up + data.down else False

    def _does_switch_optimal() -> bool:
        return True if abs(data.current_floor - current_target) > abs(data.current_floor - abs_floor) else False

    def _valid_direction() -> bool:
        return True if (state == State.UP.name and floor >= 0 and
                        abs_floor < data.current_floor < abs(current_target)) or \
                       (state == State.DOWN.name and floor < 0 and
                        abs_floor > data.current_floor > abs(current_target)) else False

    conditions = [
        state not in (State.IDLE.name, State.VIP.name),
        abs_floor in range(left_limit, right_limit + 1),
        current_target not in (abs_floor, math.inf),
        data.switches > 0,
        data.current_floor != floor,
        _valid_direction(),
        _does_switch_optimal(),
        _has_same_direction()
    ]

    return True if all(conditions) else False
