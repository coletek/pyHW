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
from Constants import Constants
from Device import Device

class MotorDc(Device):

    dir_pin = 0
    pwm_pin = 0
    pwm_freq = Constants.FREQ_MOTOR
    direction = False
    speed = 0

    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.is_active = True
        self.set(False, 1.0)
        
    def stop(self):
        self.set(False, 0.0)
        self.is_active = False
        
    def set(self, direction, speed):
        self.direction = direction
        self.speed = speed

        if self.hw.is_simulation:
            logger.info("direction=%d speed=%f" % (direction, speed))
        else:
            if direction:
                self.hw.gpio_write(self.dir_pin, True)
            else:
                self.hw.gpio_write(self.dir_pin, False)
            self.hw.gpio_pwm(self.pwm_pin, self.pwm_freq, self.speed * 255)
