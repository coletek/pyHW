import sys
import random
import unittest.mock
from logger_config import logger

class GPIOController:
    
    _instance = None

    is_simulation = False

    # gpio read helpers
    frequency_count = 4
    frequency = {}
    previous_time = {}
    pulse_count = {}
    pulse_times = {}
    gpio_read_callback_ref = {}
    gpio_read_callback_sim_ref = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, is_simulation = False):
        if hasattr(self, 'pi'):        
           return
       
        if not is_simulation:
            try:
                import pigpio
                self.pi = pigpio.pi()
            except:
                logger.debug("no pigpio found - assuming simulator")
                is_simulation = True

        self.is_simulation = is_simulation
                
    def gpio_write(self, pin, value):
        logger.debug("pin=%d value=%d" % (pin, value))
        if self.is_simulation:
            pass
        else:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.write(pin, value)

    def gpio_read(self, pin):
        if self.is_simulation:
            return random.randint(0, 1)
        else:
            return self.pi.read(pin)

    def gpio_read_callback_setup(self, pin):
        if self.is_simulation:
            self.gpio_read_callback_sim_ref[pin] = threading.Timer(1, self.gpio_read_callback_sim, args=[ pin ])
            self.gpio_read_callback_sim_ref[pin].start()
        else:
            self.pi.set_mode(pin, pigpio.INPUT)
            self.gpio_read_callback_ref[pin] = self.pi.callback(pin, pigpio.RISING_EDGE, self.gpio_read_callback)
        self.pulse_times[pin] = []

    def gpio_read_callback_stop(self, pin):
        if self.is_simulation:
            self.gpio_read_callback_sim_ref[pin].stop()
        else:
            self.gpio_read_callback_ref[pin].cancel()
        
    def gpio_read_callback_sim(self, pin):
        self.pulse_count[pin] += 1
        current_time = time.clock_gettime(time.CLOCK_MONOTONIC)
        if self.pulse_count[pin] > 1:
            self.pulse_times[pin].append(current_time - self.previous_time[pin])
            if len(self.pulse_times[pin]) > self.frequency_count:
                self.pulse_times[pin].pop(0)
            self.frequency[pin] = self.frequency_count / sum(self.pulse_times[pin])
        self.previous_time[pin] = current_time
        self.gpio_read_callback_sim_ref[pin] = threading.Timer(1, self.gpio_read_callback_sim, args=[ pin ])
        self.gpio_read_callback_sim_ref[pin].start()
        logger.debug("pin=%d count=%d freq=%f" % (pin, self.pulse_count[pin], self.frequeny[pin]))
        
    def gpio_read_callback(self, gpio, level, tick):
        self.pulse_count[gpio] += 1
        current_time = time.time()
        if self.pulse_count[gpio] > 1:
            self.pulse_times[gpio].append(current_time - self.previous_time[gpio])
            if len(self.pulse_times[gpio]) > self.frequency_count:
                self.pulse_times[gpio].pop(0)
            self.frequency[gpio] = self.frequency_count / sum(self.pulse_times[gpio])
        self.previous_time[gpio] = current_time
        logger.debug("pin=%d count=%d freq=%f" % (gpio, self.pulse_count[gpio], self.frequeny[gpio]))
        
    def gpio_pwm(self, pin, freq, dutycycle):
        logger.debug("pin=%d dutycycle=%d" % (pin, dutycycle))
        if self.is_simulation:
            pass
        else:
            self.pi.set_mode(pin, pigpio.OUTPUT)
            self.pi.set_PWM_frequency(pin, freq)
            self.pi.set_PWM_dutycycle(pin, dutycycle)

    def serial_open(self, port, baud_rate):
        logger.debug("port=%s baud_rate=%d" % (port, baud_rate))
        if self.is_simulation:
            pass
        else:
            self.serial_fd = self.pi.serial_open(port, baud_rate)

    def serial_close(self):
        if self.is_simulation:
            pass
        else:
            self.pi.serial_close(self.serial_fd)
            
    def serial_read(self):
        if self.is_simulation:
            length = random.randint(1, 8)
            return bytearray([random.randint(0, 255) for _ in range(length)])
        else:
            data = self.pi.serial_read(self.serial_fd)
            return data.decode("utf-8").strip()

    def serial_write(self, data):
        hex_string = "".join("{:02x}".format(b) for b in data)
        logger.debug("data=0x%s (%s)" % (format(hex_string), data))
        if self.is_simulation:
            pass
        else:
            self.pi.serial_write(self.serial_fd, data.encode("utf-8"))

    def spi_open(self, port):
        logger.debug("port=%d" % (port))
        if self.is_simulation:
            pass
        else:
            self.spi_fd = self.pi.spi_open(0, port)

    def spi_close(self):
        if self.is_simulation:
            pass
        else:
            self.pi.spi_close(self.spi_fd)
            
    def spi_read(self):
        if self.is_simulation:
             response = bytearray([random.randint(0, 255) for _ in range(8)])
             return response
        else:
            data = self.pi.spi_read(self.spi_fd, 1)
            return data

    def spi_write(self, data):
        hex_string = "".join("{:02x}".format(b) for b in data)
        logger.debug("data=0x%s" % hex_string)
        if self.is_simulation:
            pass
        else:
            self.pi.spi_write(self.spi_fd, data)
            self.pi.spi_close(self.spi_fd)

    def i2c_open(self, port, address):
        logger.debug("port=%d address=0x%02x" % (port, address))
        if self.is_simulation:
            pass
        else:
            self.i2c_fd = pi.i2c_open(port, address)

    def i2c_close(self):
        if self.is_simulation:
            pass
        else:
            self.pi.i2c_close(self.i2c_fd)
            
    def i2c_read(self):
        if self.is_simulation:
            length = random.randint(1, 10)
            return bytearray([random.randint(0, 255) for _ in range(length)])
        else:
            data = self.pi.i2c_read_device(self.i2c_fd, 1)
            self.pi.i2c_close(self.i2c_fd)
            return data

    def i2c_write(self, data):
        hex_string = "".join("{:02x}".format(b) for b in data)
        logger.debug("data=0x%s" % hex_string)
        if self.is_simulation:
            pass
        else:
            self.pi.i2c_write_device(self.i2c_fd, data)

    def one_wire_open(self):
        path = "/sys/devices/w1_bus_master1/w1_master_slaves"
        logger.debug("path=%s" % path)
        if self.is_simulation:
            pass
        else:
            self.one_wire_fd = pi.bf_gen(path)

    def one_wire_close(self):
        if self.is_simulation:
            pass
        else:
            pi.bf_clear(self.one_wire_fd)

    def one_wire_read_temperatures(self):
        if self.is_simulation:
            temperatures = []
            length = random.randint(0, 32)
            for d in range(length):
                temperatures.append(random.randint(-200, 200))
            return temperatures
        else:
            temperatures = []
            for device_id in pi.w1_scan(self.one_wire_fd):
                temperature = pi.w1_read_temp(self.one_wire_fd + device_id)
                temperatures.append(temperature)
            return temperatures

    def stop(self):
        if not self.is_simulation:
            self.pi.stop()
