import pins
from log import init_global_logger, global_logger

PRINT_LOGGING = True

def main() -> None:
    running = False
    last = False
    last_T = 0.0

    global_logger().write_info("start main()")
    while True:
        T = pins.thermocouple.temperature

        # if temperature has changed enough, write log entry
        if abs(T-last_T) > 0.5:
            global_logger().write_info(f"T: {T:.2f}°C")
            last_T = T

        if PRINT_LOGGING: 
            print(f"T: {T:.2f}°C", end ='\r')
            sleep(0.5)
        
        running = bool(pins.run_pin.state)
        if last == running: continue

        global_logger().write_info(f"set state to {running}")
        if PRINT_LOGGING: print(f"Set state to {running}")

        pins.valve.set(running)
        pins.mosfet.set(running)
        
        last = running

if __name__ == "__main__":
    init_global_logger(folder="logs/", print_log=PRINT_LOGGING)
    try:
        main()
    except Exception as e:
        global_logger().write_error(f"System exit with exception {e}")
        pass
    finally:
        global_logger().write_info("System exit")
        pins.board.reset()