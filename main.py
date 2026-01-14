import pins

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