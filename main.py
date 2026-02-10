import pins
# from log import init_global_logger, global_logger


def main() -> None:
    running = False
    last = False

    # global_logger().write_info("start main()")
    while True:
        print(pins.thermocouple.temperature)

        running = pins.run_pin.state
        if last == running: continue

        if running:
            # run loop
            pins.pump.set_on()
            pins.valve.set_on()
            pins.mosfet.set_on()
        else:
            # don't
            pins.pump.set_off()
            pins.valve.set_off()
            pins.mosfet.set_off()
        
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