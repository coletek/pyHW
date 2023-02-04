from logger_config import logger

import GPIOController

gpio = GPIOController.GPIOController()

gpio.gpio_write(1, 0)
data = gpio.gpio_read(1)
logger.info("gpio_read=%d" % data)

gpio.serial_open("/dev/ttyS0", 9600)
data = bytearray([0x01, 0x02, 0x03, 0x04])
gpio.serial_write(data)
data = gpio.serial_read()
hex_string = "".join("{:02x}".format(b) for b in data)
logger.info("serial_read=0x%s (%s)" % (format(hex_string), data))
gpio.serial_close()

gpio.spi_open(0)
data = bytearray([0x01, 0x02, 0x03, 0x04])
gpio.spi_write(data)
data = gpio.spi_read()
hex_string = "".join("{:02x}".format(b) for b in data)
logger.info("spi_read=0x%s" % format(hex_string))
gpio.spi_close()

gpio.i2c_open(0, 0x00)
data = bytearray([0x01, 0x02, 0x03, 0x04])
gpio.i2c_write(data)
data = gpio.i2c_read()
hex_string = "".join("{:02x}".format(b) for b in data)
logger.info("i2c_read=0x%s" % format(hex_string))
gpio.i2c_close()

gpio.one_wire_open()
data = gpio.one_wire_read_temperatures()
temps = ", ".join("{:02d}".format(b) for b in data)
logger.info("one_wire_read_temperatures=%s" % temps)
gpio.one_wire_close()
