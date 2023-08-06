"""
pi_shiftreg.

A simple tool for controlling Shift Registers with RPi GPIO pins

Call init_state() before using set_state()
"""

__version__ = "0.1.0"
__author__ = 'Kevin Thorne'


import RPi.GPIO as GPIO
import time

# State
_state_to_apply = []
_current_state = ()

# Config
_clock_pin = None
_data_pin = None
_applicator_pin = None
_write_state_out_to = None
_applicator_delay = 0


def init_state(register_count: int,
               clock_pin: int,
               data_pin: int,
               applicator_pin: int,
               init_val: bool = False,
               write_state_out_to = None,
               applicator_delay = 0):
    """
    Set up the module to use [set_state]

    :param register_count: how many registers to configure
    :param clock_pin: set the clock pin
    :param data_pin: set the data pin
    :param applicator_pin: set the applicator pin
    :param init_val (optional): set the initial value on each register (default: False)
    :param write_state_out_to (optional): write state to file after application (default: no file)
    :param applicator_delay (optional): cooldown delay between applications (is blocking, default: 0)
    """
    global _current_state, _state_to_apply
    global _clock_pin, _data_pin, _applicator_pin, _write_state_out_to, _applicator_delay
    new_current_state = []
    _state_to_apply = []

    _clock_pin = clock_pin
    _data_pin = data_pin
    _applicator_pin = applicator_pin
    _applicator_delay = applicator_delay

    GPIO.setmode(GPIO.BCM)

    GPIO.setwarnings(False)
    GPIO.setup(_data_pin, GPIO.OUT)
    GPIO.setup(_clock_pin, GPIO.OUT)
    GPIO.setup(_applicator_pin, GPIO.OUT)
    GPIO.setwarnings(True)

    for i in range(0, register_count):
        new_current_state.append(init_val)
        _state_to_apply.append(init_val)

    _current_state = tuple(new_current_state)
    _write_state_out_to = write_state_out_to


def set_current_state(state: list):
    """
    Set the states of all available registers

    :param states: array of True/False
    """
    if len(state) != len(_current_state):
        raise ValueError(
            "State array given does not match the size of registers configured")
    for i in range(0, len(_current_state)):
        set_state(i, state[i], apply_immediately=False)
    _apply()


def set_state(idx: int, to: bool, apply_immediately: bool = True):
    """
    Set the state of the register given [idx]

    :param idx: index of register
    :param to: new value of register
    :param apply_immediately (optional): optionally defer application
    """
    assert isinstance(to, bool)
    assert idx < len(_current_state)
    _state_to_apply[idx] = to

    if apply_immediately:
        _apply()


def get_current_state() -> tuple:
    return _current_state


def _apply():
    """
    Takes the `state_to_apply` list and applies it, setting
    `current_state` in return
    """
    global _current_state
    assert len(_current_state) != 0
    assert len(_state_to_apply) == len(_current_state)
    assert _applicator_pin
    assert _clock_pin
    assert _data_pin

    GPIO.output(_applicator_pin, 0)
    for val in _state_to_apply:
        GPIO.output(_data_pin, 1 if val else 0)
        GPIO.output(_clock_pin, 1)
        GPIO.output(_clock_pin, 0)
    GPIO.output(_applicator_pin, 1)

    _current_state = tuple(_state_to_apply)
    if _write_state_out_to:
        with open(_write_state_out_to, mode='w') as f:
            f.write(_current_state)

    time.sleep(_applicator_delay)
