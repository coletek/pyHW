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

# TODO: upgrade to GPIOController
import serial
import math

class RION(Device):

    model = "LCA"
    port = "/dev/ttyS0"
    baudrate = 9600
    uart_dev = ""

    def start(self):
        self.is_active = True
        
        try:
            self.uart_dev = serial.Serial(self.port, baudrate=self.baudrate, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
            #self.uart_dev = serial.Serial(port, baudrate=baudrate)
        except:
            logger.debug("no serial - assuming simulator")
            self.is_simulator = True

    def read_angles(self):
        if self.is_simulator:
            return
        
        n = self.uart_dev.write(serial.to_bytes([0x68, 0x04, 0x00, 0x04, 0x08]))
        
        data = self.uart_dev.read(2)
        
        if len(data) < 2:
            print (data)
            return -1, 0, 0
        
        datalen = data[1]
        data = self.uart_dev.read(data[1] - 1)
        if len(data) < 5:
            print (data)
            return -1, 0, 0

        if self.model == "LCA":
            if data[2] == 0x10:
                x = "-%x.%x" % (data[3], data[4])
            else:
                x = "%x.%x" % (data[3], data[4])
            if data[5] == 0x10:
                y = "-%x.%x" % (data[6], data[7])
            else:
                y = "%x.%x" % (data[6], data[7])
        elif self.model == "HCA":
            if data[2] == 0x10:
                x = "-%x.%x%x" % (data[3], data[4], data[5])
            else:
                x = "%x.%x%x" % (data[3], data[4], data[5])
            if data[6] == 0x10:
                y = "-%x.%x%x" % (data[7], data[8], data[9])
            else:
                y = "%x.%x%x" % (data[7], data[8], data[9])
        else:
            return -1, 0, 0
            
        return 0, math.radians(float(x)), math.radians(float(y))
