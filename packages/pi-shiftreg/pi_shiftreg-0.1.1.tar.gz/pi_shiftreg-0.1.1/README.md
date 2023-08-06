# pi_shiftreg

A simple Python 3 tool for controlling Shift Registers with RPi GPIO pins.

## Installation
Use PIP:
```
pip install pi_shiftreg
```

## Usage

### init_state
```
    Set up the module to use [set_state]
    :param register_count: how many registers to configure
    :param clock_pin: set the clock pin
    :param data_pin: set the data pin
    :param applicator_pin: set the applicator pin
    :param init_val (optional): set the initial value on each register (default: False)
    :param write_state_out_to (optional): write state to file after application (default: no file)
    :param applicator_delay (optional): cooldown delay between applications (is blocking, default: 0)
```
Example:
```python
import pi_shiftreg
pi_shiftreg.init_state(24, 17, 18, 27, write_state_out_to="myfile.txt")
```

### set_state
```
    Set the state of the register given [idx]
    :param idx: index of register
    :param to: new value of register
    :param apply_immediately (optional): optionally defer application
```
Example:
```python
# call init_state prior
pi_shiftreg.set_state(1, True) # set register 1 to True (1)
```