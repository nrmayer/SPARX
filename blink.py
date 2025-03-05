from automation import *
import time

board = Automation2040W()

while (1):
    board.conn_led(True)
    time.sleep(0.5)
    board.conn_led(False)
    time.sleep(0.5)