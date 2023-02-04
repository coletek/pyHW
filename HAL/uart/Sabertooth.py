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
import Constants
from Device import Device

 # upgrade to GPIOController
import time
import serial

class Sabertooth(Device):

    address = 128
    uart_dev = ""
    baudrate = 9600

    def start(self, address = 128, port = "/dev/ttyS0", baudrate = 9600):
        
        self.address = address

        try:
            self.uart_dev = serial.Serial(port, baudrate)
        except:
            logger.debug("no serial - assuming simulator")
            self.is_simulator = True

        # auto set baud rate (for V1 only) - really really bad - http://webbot.org.uk/WebbotLibDocs2/44218.html
        #time.sleep(2)
        #n = self.uart_dev.write(bytes(chr(170), 'UTF-8')) 
        
        time.sleep(1)

    def motor_control_left(self, speed): # speed: -127 to 127
        if speed >= 0:
            command = 0
        elif speed < 0:
            command = 1
            speed = - speed
        if speed > 127:
            speed = 127
        self.send_motor_command(self.address, command, speed)  

    def motor_control_right(self, speed): # speed: -127 to 127
        if speed >= 0:
            command = 4
        elif speed < 0:
            command = 5
            speed = - speed
        if speed > 127:
            speed = 127
        self.send_motor_command(self.address, command, speed)  

    def motor_control(self, speed_left, speed_right):
        self.motor_control_left(speed_left)
        self.motor_control_right(speed_right)
        
    def send_motor_command(self, address, command, speed):
        if self.is_simulator:
            return
            
        checksum = (address + command + speed) & 0b01111111
        print ("send_motor_command (addr, cmd, speed, checksum): ", address, command, speed, checksum)

        # python2
        #n = self.uart_dev.write(chr(address))
        #n = self.uart_dev.write(chr(command))
        #n = self.uart_dev.write(chr(speed))
        #n = self.uart_dev.write(chr(checksum))
        
        # python3
        n = self.uart_dev.write(bytes(chr(address), 'UTF-8'))
        n = self.uart_dev.write(bytes(chr(command), 'UTF-8'))
        n = self.uart_dev.write(bytes(chr(speed), 'UTF-8'))
        n = self.uart_dev.write(bytes(chr(checksum), 'UTF-8'))
