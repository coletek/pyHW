# pyRPI
# Copyright (C) 2017-2023 Luke Cole
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import sys
import time
from logger_config import logger
import GPIOController
import Constants
from Device import Device

try:
    import spidev # move to using GPIOController
except:
    pass
    
class MAX7301ATL(Device):

    is_simulator = False
    
    def start(self):
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(0, 0)
        
            register = 0x04
            content = 0x01 # normal operation
            self.spi.max_speed_hz = 1000000
            self.spi.xfer2([register, content])
        except:
           logger.debug("no serial - assuming simulator")
           self.is_simulator = True

    def set_all_io_output_and_low(self):
        for pin in range(4, 31+1):
            self.set_pin_as_output(pin)
            self.set_pin(pin, 0)
            
    def print_status(self, pin):
        conf_register = self.get_conf_register_for_pin(pin)
        conf_content = self.read_register(conf_register)
        time.sleep(0.1)
        value_register = self.get_value_register_for_pin(pin)
        value_content = self.read_register(value_register)
        print ("pin=%d: conf_register[0x%02x]=%s value_register[0x%02x]=%d" % (pin, conf_register, str(bin(conf_content)), value_register, value_content))        

    def print_status_all(self):
        for pin in range(4, 31+1):
            self.print_status(pin)

    def set_pin_as_input(self, pin, pullup = True):
        if self.is_simulator:
            return
        
        register = self.get_conf_register_for_pin(pin)
        content = self.read_register(register)
        content &= ~(0b11 << self.get_bit_shift_for_pin(pin))
        if pullup:
            content |= 0b11 << self.get_bit_shift_for_pin(pin)
        else:
            content |= 0b10 << self.get_bit_shift_for_pin(pin)
        self.spi.xfer2([register, content])
        
    def set_pin_as_output(self, pin):
        if self.is_simulator:
            return
        
        register = self.get_conf_register_for_pin(pin)
        content = self.read_register(register)
        content &= ~(0b11 << self.get_bit_shift_for_pin(pin))
        content |= 0b01 << self.get_bit_shift_for_pin(pin)
        self.spi.xfer2([register, content])
        
    def read_register(self, register):
        if self.is_simulator:
            return
        
        self.spi.xfer2([0x80 | register, 0x00])
        content = self.spi.xfer2([0x80, 0x00])[1]
        return content
    
    def get_bit_shift_for_pin(self, pin):
        return ((pin % 4) * 2)

    def get_conf_register_for_pin(self, pin):
        return (pin - 4) // 4 + 0x09

    def get_value_register_for_pin(self, pin):
        return 0x20 + pin

    def set_pin(self, pin, value):
        if self.is_simulator:
            return
        
        register = self.get_value_register_for_pin(pin)
        self.spi.xfer2([register, value])

    def get_pin(self, pin):
        register = self.get_value_register_for_pin(pin)
        value = self.read_register(register)
        return value
