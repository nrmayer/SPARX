"""`QwiicDriver` class provides interface for `machine.I2C` and derivatives to interface with qwiic_i2c systems

functionality taken from https://github.com/sparkfun/Qwiic_I2C_Py/blob/master/qwiic_i2c/micropython_i2c.py
"""

from machine import I2C

class QwiicDriver:
    """Wrapper for `machine.I2C` to interface with qwiic systems
    
    Implements read and write for bytes, words, and chunks over I2C

    Compatable with SparkFun's qwiic libraries
    """

    def __init__(self, driver:I2C):
        # use provided machine.I2C driver
        # NOTE: Automation2040W.i2c from Pimoroni is derived from machine.I2C
        if driver is None: raise Exception("I2C driver not provided")
        self._driver = driver


    # for use with ```with``` statements
    def __enter__(self) -> "QwiicDriver":
        return self
    
    def __exit__(self, *args, **kwargs) -> None:
        pass


    # platform checking
    # done only for compatability with other qwiic systems
    @classmethod
    def isPlatform(cls) -> bool:
        return True
    @classmethod
    def is_platform(cls) -> bool:
        return True

    # read commands

    # word reading
    def readWord(self, address:int, mem_addr:int|None=None) -> int:
        buffer: bytes
        if mem_addr is None:
            buffer = self._driver.readfrom(address, 2)
        else:
            buffer = self._driver.readfrom_mem(address, mem_addr, 2)
        
        return (buffer[1] << 8) | buffer[0]
    
    def read_word(self, address:int, command_code:int|None=None) -> int:
        return self.readWord(address, command_code)
    
    
    # byte reading
    def readByte(self, address:int, mem_addr:int|None=None) -> int:
        if mem_addr is None:
            return self._driver.readfrom(address, 1)[0]
        return self._driver.readfrom_mem(address, mem_addr, 1)[0]
    
    def read_byte(self, address:int, mem_addr:int|None=None) -> int:
        return self.readByte(address, mem_addr)
    

    # block reading
    def readBlock(self, address:int, mem_addr:int|None=None, num_bytes:int=1) -> bytes:
        if mem_addr is None:
            return self._driver.readfrom(address, num_bytes)
        return self._driver.readfrom_mem(address, mem_addr, num_bytes)
    
    def read_block(self, address:int, mem_addr:int|None=None, num_bytes:int=1) -> bytes:
        return self.readBlock(address, mem_addr, num_bytes)
    

    # write commands

    # single command writing
    def writeCommand(self, address:int, command:int) -> None:
        self._driver.writeto(address, command.to_bytes(1, 'little'))

    def write_command(self, address:int, command:int) -> None:
        self.writeCommand(address, command)


    # word writing
    def writeWord(self, address:int, memaddr:int, value:int) -> None:
        self._driver.writeto_mem(address, memaddr, value.to_bytes(2, 'little'))

    def write_word(self, address:int, memaddr:int, value:int) -> None:
        self.writeWord(address, memaddr, value)


    # byte writing
    def writeByte(self, address:int, memaddr:int, value:int) -> None:
        # length different from writeWord
        self._driver.writeto_mem(address, memaddr, value.to_bytes(1, 'little'))

    def write_byte(self, address:int, memaddr:int, value:int) -> None:
        self.writeByte(address, memaddr, value)


    # block writing
    def writeBlock(self, address:int, memaddr:int, value:int) -> None:
        self._driver.writeto_mem(address, memaddr, bytes(value))

    def write_block(self, address:int, memaddr:int, value:int) -> None:
        self.writeBlock(address, memaddr, value)


    # write-read
    def writeReadBlock(self, address:int, write_bytes:int, read_bytes:int) -> bytes:
                    # keeps i2c bus open for subsequent read vv
        self._driver.writeto(address, bytes(write_bytes), False)
        return self._driver.readfrom(address, read_bytes)
    
    def write_read_block(self, address:int, write_bytes:int, read_bytes:int) -> bytes:
        return self.writeReadBlock(address, write_bytes, read_bytes)
    

    # connection checking
    def isDeviceConnected(self, device_address:int) -> bool:
        try:
            # faster than running a full scan
            # throws IO exception if device is not connected
            self._driver.writeto(device_address, bytearray())
            return True
        except Exception:
            return False
        
    def is_device_connected(self, device_address:int) -> bool:
        return self.isDeviceConnected(device_address)
    
    def ping(self, device_address:int) -> bool:
        return self.isDeviceConnected(device_address)
    

    # scan I2C bus
    def scan(self) -> list[int]:
        return self._driver.scan()