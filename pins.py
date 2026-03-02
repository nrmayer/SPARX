"""Constant definitions for pins and drivers"""

import automation

#######################################
#######################################

THERMOCOUPLE_ENALED = True
THERMOCOUPLE_ADDRESS = 0x60

VALVE_RELAY = 0
MOSFET_RELAY = 1

RUN_PIN = automation.INPUT_1

#######################################

board = automation.Automation2040W()

if THERMOCOUPLE_ENALED:
    from thermocouple import MCP9600
    thermocouple = MCP9600(board.i2c, address=THERMOCOUPLE_ADDRESS)

# Pin class
class Pin:
    pin_num:int

    def __init__(self, pin_num:int, type):
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

# Class handler for Pimoroni builtin relay
class Relay:
    relay_num:int

    def __init__(self, num:int):
        self.relay_num = num

    def set_on(self):
        board.actuate_relay(self.relay_num)

    def set_off(self):
        board.release_relay(self.relay_num)

    def set(self, state:bool):
        self.set_on() if state else self.set_off()

# pin definitions
run_pin = Pin(RUN_PIN, "READ")
# on relay 1
valve = Relay(VALVE_RELAY)
mosfet = Relay(MOSFET_RELAY)