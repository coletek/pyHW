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

class Interrupt(Device):

    is_interrupt = False

    def __init__(self):
        self.hw = GPIOController.GPIOController()

    def start(self):
        self.hw.gpio_read_callback_setup(self.pin)

    def stop(self):
        self.hw.gpio_read_callback_stop(self.pin)
        
    def interrupt_callback(self):
        # TODO: set this if the callback was trigger - currently the callback code is targeting pulse stats
        self.is_interrupt = True
