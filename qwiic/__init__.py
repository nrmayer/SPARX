"""I2C interface for SparkFun's Qwiic family of boards

Meant to provide common I2C interfaces between board types

This project implements only needed interfaces (in this case for `machine.I2C` and derivatives)

Based on <https://github.com/sparkfun/Qwiic_I2C_Py/blob/master/qwiic_i2c/>
"""

from .driver import *