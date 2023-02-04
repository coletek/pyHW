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

# TODO: move to GPIOController
try:
    from spidev import SpiDev
except:
    pass

class MCP3008(Device):

    bus = 0
    device = 0
    bus_speed = 500000 # 500kHz
    
    def start(self):
        self.is_active = True
        
        try:
            self.spi = SpiDev()
            self.open(self.bus, self.device)
            self.spi.max_speed_hz = self.bus_speed
        except:
            logger.debug("no serial - assuming simulator")
            self.is_simulator = True

    def read(self, channel = 0):
        if self.is_simulator:
            return
        adc = self.spi.xfer2([1, (8 + channel) << 4, 0])        
        data = ((adc[1] & 3) << 8) + adc[2]
        return data
            
    def close(self):
        if self.is_simulator:
            return
        self.spi.close()
