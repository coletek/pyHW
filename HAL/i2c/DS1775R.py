# pyHW
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

from logger_config import logger
import GPIOController
from Constants import Constants
from Device import Device

# upgrade to GPIOController
import random
try:
    import RPi.GPIO as GPIO # TODO: upgrade to pigio
except:
    pass

class DS1775R(Device):
    
    bus = 1

    temperature = 0.0
    
    ADDRESS = 0x48
    REG_TEMP = 0x00
    
    def start(self):
        self.is_active = True
        
        try:
            pigpio.exceptions = True
            self.pi = pigpio.pi()
            self.fd = self.pi.i2c_open(self.bus, self.ADDRESS)
        except:
            logger.debug('no RPi.GPIO - assuming simulator')
            self.is_simulator = True

    def tick(self):
        if self.is_simulator:
            self.temperature = random.randrange(0, 100, 1)
        else:
            self.temperature = self.pi.i2c_read_byte_data(self.fd, self.REG_TEMP)
