import pins
import log

"""
Program entry point
Called from main.py at project root when microcontroller boots
"""

log.set_logger(log.Logger.new_file("logs/"))
logger = log.get_named_logger(__name__)

@logger.log_exception()
def run() -> None:
    while True:
        if pins.RUN_PIN.state == True:
            # run loop
            if not pins.pump.state:
                pins.pump.set_on()
        else:
            # don't
            if pins.pump.state:
                pins.pump.set_off()