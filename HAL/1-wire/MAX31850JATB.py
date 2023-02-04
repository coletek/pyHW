# pyHW
# Copyright (C) 2020-2023 Luke Cole
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
import glob

class MAX31850JATB(Device):

    # genarates path for perticular function
    def file_path_gen(self, sensor_id):
        base_dir = '/sys/bus/w1/devices/w1_bus_master'	# commo path
        base_dir = base_dir + str(sensor_id) + '/'	# different path for each sensor
        device_folder = sorted(glob.glob(base_dir + '3b*'))	# destination folder
        return device_folder
        #device_file = device_folder + '/w1_slave'	# destination file
        #return device_file

    # reads the lines of the 'w1_slave' file
    def temp_raw(self, file_path):
        debug.logger.debug("%s opening for reading" % file_path)
        f = open(file_path, 'r')
        debug.logger.debug("%s readlines" % file_path)
        lines = f.readlines()
        f.close()
        return lines

    # to calculate temperature from the data
    def read_temp(self, file_path):
        lines = self.temp_raw(file_path)
        # if data reading fail then wait for 0.2 second and read again
        while lines[0].strip()[-3:] != 'YES':
            debug.logger.debug("%s waiting for CRC to be yes" % file_path)
            time.sleep(0.2)
            lines = self.temp_raw()
        # find 't=' in the lines and take the data after it
        temp_output = lines[1].find('t=')
        if temp_output != -1:
            temp_string = lines[1].strip()[temp_output+2:]
            temp_c = float(temp_string) / 1000.0                        
            return temp_c
