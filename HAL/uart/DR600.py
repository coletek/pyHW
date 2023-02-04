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

from logger_config import logger
import GPIOController
import Constants
from Device import Device

# TODO: upgrade to GPIOController
import time
try:
    import pigpio
except:
    pass

class DR600(Device):

    speed = 0
    timestamp = 0
    serial_data = []
    
    setup_messages = [
        "set RS 43\r\n",
        "set RA 43\r\n", 
        "set UN 1\r\n", 
        "set LO 0\r\n", 
        "set HI 331\r\n", 
        "set SP 85\r\n", 
        "set SF 0\r\n", 
        "set ST 99\r\n", 
        "set MO 1026\r\n", 
        "set MD 261\r\n", 
        "set IO 0\r\n", 
        "set HT 0\r\n", 
        "set BN 5\r\n", 
        "set TA 30\r\n", 
        "set TR 33667\r\n", 
        "set CY 500\r\n"
    ]
    
    def __init__(self):
        try:
            pigpio.exceptions = True
            self.pi = pigpio.pi()
            self.fd = self.pi.serial_open('/dev/ttyS0', 115200, 0)
        except:
            logger.debug("no pigpio - assuming simulator")
            self.is_simulator = True
            
    def setup(self):
        logger.debug('')
        if self.is_simulator:
            return
    
        for m in self.setup_messages:
            self.pi.serial_write(self.fd, m)
            time.sleep(1)
    
    def tick(self):
        logger.debug('')
        if self.is_simulator:
            return
    
        (b, d) = self.pi.serial_read(self.fd, 1)
        if b > 0:
            data = list(d)
            for c in data:
                if chr(c) == '\n' or chr(c) == '\r':
                    speed = "".join(self.serial_data)
                    timestamp = time.time()
                    logger.debug("speed=%s" % (speed))
                    if speed != "" and speed.isdigit():
                        self.speed = int(speed)
                    else:
                        self.speed = 0
                        self.serial_data = []
                else:
                    self.serial_data.append(chr(c))
