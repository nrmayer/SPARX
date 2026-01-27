import pins
from log import init_global_logger, global_logger

def main() -> None:
    global_logger().write_info("start main()")
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
    init_global_logger(folder="logs/")
    try:
        main()
    except Exception as e:
        global_logger().write_error(f"System exit with exception {e}")
    finally:
        global_logger().write_info("System exit")
        pins.board.reset()