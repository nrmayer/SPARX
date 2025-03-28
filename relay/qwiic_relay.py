#-----------------------------------------------------------------------------
# qwiic_relay.py
#
# Python library for the SparkFun Qwiic Relays
#
#   https://www.sparkfun.com/products/15168
#
#------------------------------------------------------------------------
#
# Written by  SparkFun Electronics, July 2019
#
# This python library supports the SparkFun Electronics qwiic
# qwiic sensor/board ecosystem
#
# More information on qwiic is at https:// www.sparkfun.com/qwiic
#
# Do you like this library? Help support SparkFun. Buy a board!
#
#----------------------------------------------------------------------------
# 
# Modified by Noah (SPARX), March 2025
# Added method to set relay state with `bool` parameter instead of using
# `set_relay_on()` and `set_relay_off()`
#
#==================================================================================
# Copyright (c) 2019 SparkFun Electronics
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#==================================================================================
#
# This is mostly a port of existing Arduino functionality, so pylint is sad.
# The goal is to keep the public interface pythonic, but internal is internal
#
# pylint: disable=line-too-long, bad-whitespace, invalid-name
#
"""
qwiic_relay
===============
Python module for the `SparkFun Qwiic Single Relay <https://www.sparkfun.com/products/15093>`_, `SparkFun Qwiic Quad Relay <https://www.sparkfun.com/products/15102>`_, `SparkFun Qwiic Dual Solid State Relay <https://www.sparkfun.com/products/16810>`_, `SparkFun Qwiic Quad Solid State Relay <https://www.sparkfun.com/products/16796>`_

This package can be used in conjunction with the overall `SparkFun qwiic Python Package <https://github.com/sparkfun/Qwiic_Py>`_

New to qwiic? Take a look at the entire `SparkFun qwiic ecosystem <https://www.sparkfun.com/qwiic>`_.

"""

from qwiic import QwiicDriver

#-----------------------------------------------------------------------------
# Define the device name and I2C addresses. These are set in the class definition
# as class variables, making them available without having to create a class instance.
# This allows higher level logic to rapidly create an index of qwiic devices at
# runtime
#
# The name of this device
_DEFAULT_NAME = "SparkFun Qwiic Relay"

# Some devices have multiple available addresses - this is a list of these addresses.
# NOTE: The first address in this list is considered the default I2C address for the
# device.
SINGLE_RELAY_DEFUALT_ADDR                = 0x18
SINGLE_RELAY_JUMPER_CLOSE_ADDR           = 0x19
QUAD_RELAY_DEFUALT_ADDR                  = 0x6D
QUAD_RELAY_JUMPER_CLOSE_ADDR             = 0x6C
DUAL_SOLID_STATE_RELAY_DEFUALT_ADDR      = 0x0A
DUAL_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR = 0x0B
QUAD_SOLID_STATE_RELAY_DEFUALT_ADDR      = 0x08
QUAD_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR = 0x09

_AVAILABLE_I2C_ADDRESSES = [
    SINGLE_RELAY_DEFUALT_ADDR,
    SINGLE_RELAY_JUMPER_CLOSE_ADDR,
    QUAD_RELAY_DEFUALT_ADDR,
    QUAD_RELAY_JUMPER_CLOSE_ADDR,
    DUAL_SOLID_STATE_RELAY_DEFUALT_ADDR,
    DUAL_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR,
    QUAD_SOLID_STATE_RELAY_DEFUALT_ADDR,
    QUAD_SOLID_STATE_RELAY_JUMPER_CLOSE_ADDR
]

# Define the register offsets of each relay
RELAY_ONE   = 1
RELAY_TWO   = 2
RELAY_THREE = 3
RELAY_FOUR  = 4

# Define register start positions
DUAL_QUAD_TOGGLE_BASE = 0x00
STATUS_BASE           = 0x04
DUAL_QUAD_PWM_BASE    = 0x0F
TURN_ALL_OFF          = 0x0A
TURN_ALL_ON           = 0x0B
TOGGLE_ALL            = 0x0C

# Special values for single relay
SINGLE_OFF              = 0x00
SINGLE_ON               = 0x01
SINGLE_FIRMWARE_VERSION = 0x04
SINGLE_STATUS           = 0x05

# Define the value of an "Off" relay
STATUS_OFF = 0

# define the class that encapsulates the device being created. All information associated with this
# device is encapsulated by this class. The device class should be the only value exported
# from this module.

class QwiicRelay:
    """
    QwiicRelay

        :param address: The I2C address to use for the device.
                        If not provided, the default address is used.
        :param i2c_driver: An existing i2c driver object. If not provided
                        a driver object is created.
        :return: The Qwiic Relay device object.
        :rtype: Object
    """
    # Constructor
    device_name         = _DEFAULT_NAME
    available_addresses = _AVAILABLE_I2C_ADDRESSES
    
    # Constructor
    def __init__(self, address, i2c_driver:QwiicDriver):

        # Did the user specify an I2C address?
        if address in self.available_addresses:
            self.address = address
        else:
            self.address = self.available_addresses[0]
        
        # Set which register map we'll use here
        
        # NOTE SPARX:
        # we don't want to automatically load
        # it won't find the platform or the i2c object if it tries
        """
        # load the I2C driver if one isn't provided
        if i2c_driver is None:
            self._i2c = qwiic_i2c.getI2CDriver()
            if self._i2c is None:
                print("Unable to load I2C driver for this platform.")
                return
        else:
            self._i2c = i2c_driver
        """

        # NOTE SPARX modification
        if i2c_driver is None:
            raise Exception("Pass in I2C driver!")

        self._i2c = i2c_driver

    # ----------------------------------
    # is_connected()
    #
    # Is an actual board connected to our system?

    def is_connected(self):
        """
            Determine if the Qwiic Relay is connected to the system.

            :return: True if the device is connected, otherwise False.
            :rtype: bool

        """
        return self._i2c.isDeviceConnected(self.address)

    connected = property(is_connected)

    # ----------------------------------
    # begin()
    #
    # Initialize the system/validate the board.
    
    def begin(self):
        """
            Initialize the operation of the relay

            :return: Returns true of the initialization was successful, otherwise False.
            :rtype: bool

        """

        # Basically return True if we are connected...

        return self.is_connected()
    
    #----------------------------------------------------------------
    # set_relay_state(relayNum, status)
    #
    # Toggles a specific relay number. If using a single relay, pass in only status

    def set_relay_state(self, state:bool, relayNum:int|None=None) -> None:
        """Toggles a specific relay number. 
        If using a single relay, pass in only `state`

        Parameters
        ----------
        state : `bool`
            The status to set the relay to
        relay_num : `int`
            The relay number to set the status of

        Returns
        -------
        null : `None`
        """

        # get status int from boolean passed in
        state_set: int = SINGLE_ON if state else SINGLE_OFF

        if relayNum is None:
            self._i2c.writeCommand(self.address, state_set)
        else:
            temp = self._i2c.readByte(self.address, STATUS_BASE + relayNum)
            if temp == STATUS_OFF:
                self._i2c.writeCommand(self.address, DUAL_QUAD_TOGGLE_BASE + relayNum)

    #----------------------------------------------------------------
    # set_relay_on(relayNum)
    #
    # Turn's on a specific relay number, if we're using a single relay, do not pass in a relay number.
    
    def set_relay_on(self, relayNum=None):
        """
            Turns on a relay,if we're using a single relay, do not pass in a relay number

            :param: The relay to turn on
            :return: successful I2C transaction
            :rtype: bool
        """
        self.set_relay_state(True, relayNum)

    #----------------------------------------------------------------
    # set_relay_off(relayNum)
    #
    # Turn's off a specific relay number, if we're using a single relay, do not pass in a relay number.
    
    def set_relay_off(self, relayNum=None):
        """
            Turns off a relay,if we're using a single relay, do not pass in a relay number

            :param: The relay to turn off
            :return: successful I2C transaction
            :rtype: bool
        """
        self.set_relay_state(False, relayNum)
        

    #----------------------------------------------------------------
    # set_all_relays_on(relayNum)
    #
    # Turn's on all relays. This command does nothing for the single relay    
    def set_all_relays_on(self):
        """
            Turns on all relays. This command does nothing for the single relay
            
            :param: The relay to turn on
            :return: successful I2C transaction
            :rtype: bool
        """
        
        return self._i2c.writeCommand(self.address, TURN_ALL_ON)
    
    #----------------------------------------------------------------
    # set_all_relays_off(relayNum)
    #
    # Turn's off all relays. This command does nothing for the single relay
    
    def set_all_relays_off(self):
        """
            Turns off all relays. This command does nothing for the single relay
            
            :param: The relay to turn off
            :return: successful I2C transaction
            :rtype: bool
        """
        
        return self._i2c.writeCommand(self.address, TURN_ALL_OFF)
    
    #----------------------------------------------------------------
    # set_slow_pwm(relayNum, pwmValue)
    #
    # Sets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
    # A full cycle takes 1 second
    
    def set_slow_pwm(self, relayNum, pwmValue):
        """
            Sets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
            A full cycle takes 1 second.
            
            :param: The relay to set the PWM signal of
            :param: The value of the PWM signal, a value between 0 and 120
            :return: successful I2C transaction
            :rtype: bool
        """
        for i in range(4):
            if self.address == self.available_addresses[i]:
                print ("Slow PWM does not work for the mechanical relays")
                return False
        return self._i2c.writeByte(self.address, DUAL_QUAD_PWM_BASE + relayNum, pwmValue)
        
    #----------------------------------------------------------------
    # get_slow_pwm(relayNum)
    #
    # Gets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
  
    def get_slow_pwm(self, relayNum):
        """
            Gets the value for the slow PWM signal. Can be anywhere from 0 (off) to 120 (on).
            
            :param: The relay to get the PWM signal of
            :return: The value of the PWM signal, a value between 0 and 120
            :rtype: bool
        """
        for i in range(4):
            if self.address == self.available_addresses[i]:
                print ("Slow PWM does not work for the mechanical relays")
                return False
        return self._i2c.readByte(self.address, DUAL_QUAD_PWM_BASE + relayNum)
    
    #----------------------------------------------------------------
    # get_relay_state(relayNum)
    #
    # Returns the status of the relayNum you pass to it. Do not pass in a relay number if you are using a single relay.
    
    def get_relay_state(self, relayNum=None):
        """
            Returns true if the relay is currently on, and false if it is off.
 
            :return: Status of the relay
            :rtype: bool
        """
        
        if relayNum is None:
            relayNum = 1
        
        if self._i2c.readByte(self.address, STATUS_BASE + relayNum) is STATUS_OFF:
            return False
        else:
            return True

    #----------------------------------------------------------------
    # get_version()
    #
    # Returns the firmware version for the Single Relay

    def get_version(self):
        """
            Returns the firmware version for the Single Relay

            :return: The firmware version
            :rtype: string
        """

        return self._i2c.readByte(self.address, SINGLE_FIRMWARE_VERSION)

    version = property(get_version)