# pyHW
# Copyright (C) 2013-2023 Luke Cole
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
import cv2

class Cam(Device):

    def start(self, ch = 0):
        
        try:
            self.fd = cv2.VideoCapture(ch)
        except:
            logger.debug('VideoCapture(%d) failed - assuming simulator' % ch)
            self.is_simulator = True
      
    def tick(self):
        logger.debug('')
        if self.is_simulator:
            return
    
        ret, frame = self.fd.read()
        if ret > 0:
            self.frame = frame

    def save(self, filename):
        cv2.imwrite(filename, self.frame)
