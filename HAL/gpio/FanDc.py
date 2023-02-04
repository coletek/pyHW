# pyHW
# Copyright (C) 2018-2023 Luke Cole
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

class FanDc(Device):

    speed = 0
    pin = 0

    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.is_active = True
        self.set(1)
        
    def stop(self):
        self.set(0)
        self.is_active = False
        
    def set(self, speed):        
        self.speed = speed

        if self.hw.is_simulation:
            logger.info("speed=%f" % speed)
        else:
            self.hw.gpio_pwm(self.pin, Constants.PWM_MOTOR, self.speed * 255)
