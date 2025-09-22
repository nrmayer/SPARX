"""Static definitions for pins and drivers"""

import automation
from typing import Literal

from qwiic_driver import QwiicDriver
from qwiic_relay import QwiicRelay, SINGLE_RELAY_DEFUALT_ADDR
from pump import VaccuumPump
from thermocouple import MCP9600

# board and drivers
board = automation.Automation2040W()
qwiic_driver = QwiicDriver(board.i2c)

# do not use `_pump_relay` outside of pins.py
_pump_relay = QwiicRelay(SINGLE_RELAY_DEFUALT_ADDR, qwiic_driver)
pump = VaccuumPump(_pump_relay, 1)

thermocouple = MCP9600(board.i2c)

# Pin class
class Pin:
    pin_num:int

    type InputType = Literal["READ"] | Literal["WRITE"]

    pin_type:InputType

    def __init__(self, pin_num:int, type:InputType):
        self.pin_num = pin_num
        self.pin_type = type

    @property
    def state(self) -> int:
        return board.read_input(self.pin_num)
    
    @property
    def percent(self) -> int:
        return board.output_percent(self.pin_num)

    def set(self, val:float|bool) -> None:
        if self.pin_type == "WRITE":
            board.output(self.pin_num, val)
        else:
            raise Exception("Cannot write to readonly pin!")

# pin definitions
RUN_PIN = Pin(automation.INPUT_1, "READ")