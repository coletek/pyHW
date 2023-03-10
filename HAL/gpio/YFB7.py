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

class YFB7(Device):

    pin = 0

    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.is_active = True
        self.hw.gpio_read_callback_setup(self.pin)

    def stop(self):
        self.hw.gpio_read_callback_stop(self.pin)
        self.is_active = False
        
    def get_pulses(self):
        return self.hw.pulse_count[self.pin]

    def get_flow_rate(self): # L/min? TODO change to m^3/s
        return self.hw.frequency[self.pin] / Constants.YFB7_FLOW_RATE_TO_FREQ
