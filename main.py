import pins
import log

log.set_logger(log.Logger.new_file("logs/"))
logger = log.get_named_logger(__name__)

@logger.log_exception()
def main() -> None:
    while True:
        if pins.RUN_PIN.state == True:
            # run loop
            if not pins.pump.state:
                pins.pump.set_on()
        else:
            # don't
            if pins.pump.state:
                pins.pump.set_off()

if __name__ == "__main__":
    try:
        main()
    finally:
        pins.board.reset()