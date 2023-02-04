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

class Light(Device):

    speed = 0
    pin = 0

    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.set(True)
        
    def stop(self):
        self.set(False)
        
    def set(self, state = 0):
        if self.hw.is_simulation:
            if state == False:
                logger.info("OFF")
            else:
                logger.info("ON")
        else:
            self.hw.gpio_write(self.pin, state)

        self.is_active = state
