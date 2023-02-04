# pyRPI
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

import time
import sys
import threading

from logger_config import logger
import GPIOController
import Constants
from Device import Device

class Buzzer(Device):

    pin = 0
    
    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.set()
        self.timer = threading.Timer(1, self.stop)
        self.timer.start()
        
    def stop(self):
        time.sleep(0.1)
        if self.hw.is_simulation:
            logger.info("beep stopped")
        else:
            self.hw.gpio_pwm(self.pin, Constants.PWM_BUZZER, 0.0 * 255)
        
    def set(self):
        if self.hw.is_simulation:
            logger.info("beep started")
        else:
            self.hw.gpio_pwm(self.pin, Constants.PWM_BUZZER, 0.5 * 255)
