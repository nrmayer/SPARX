import pins
# from log import init_global_logger, global_logger


def main() -> None:
    running = False
    last = False

    # global_logger().write_info("start main()")
    while True:
        if pins.THERMOCOUPLE_ENALED:
            print(pins.thermocouple.temperature)

        running = bool(pins.run_pin.state)
        if last == running: continue

        pins.valve.set(running)
        pins.mosfet.set(running)
        
        last = running

if __name__ == "__main__":
    # init_global_logger(folder="logs/")
    try:
        main()
    except Exception as e:
        # global_logger().write_error(f"System exit with exception {e}")
        pass
    finally:
        # global_logger().write_info("System exit")
        pins.board.reset()