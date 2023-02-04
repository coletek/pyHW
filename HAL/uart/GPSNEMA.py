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

from GeographicCoordinates import *

# TODO: upgrade to GPIOController
import time
import datetime
import serial

class GPSNEMA(Device):
    """GPS NEMA"""
    
    message_preamble = '$'
    message_postamble = '\n'
    
    uart_dev = ""
    baudrate = 9600

    # https://www.sparkfun.com/datasheets/GPS/NMEA%20Reference%20Manual-Rev2.1-Dec07.pdf
    
    tmp_timestamp = 0.0
    tmp_satellites_num = 0
    tmp_satellites_in_view = 0        
    tmp_position_fix_indicator = 0
    tmp_latitude = 0.0
    tmp_longitude = 0.0
    tmp_antenna_altitude = 0.0
    tmp_course_over_ground = 0.0
    tmp_speed_over_ground = 0.0

    timestamp = 0.0
    satellites_num = 0
    satellites_in_view = 0        
    position_fix_indicator = 0
    latitude = 0.0
    longitude = 0.0
    antenna_altitude = 0.0
    course_over_ground = 0.0
    speed_over_ground = 0.0
    
    def start(self, port = "/dev/ttyS0", baudrate = 9600, timeout = 0.1):
        try:
            self.uart_dev = serial.Serial(port, baudrate, timeout = timeout)
        except:
            logger.debug("no serial - assuming simulator")
            self.is_simulator = True

        self.geo = GeographicCoordinates()

    def update(self):
        
        self.timestamp = self.tmp_timestamp
        self.satellites_num = self.tmp_satellites_num
        self.satellites_in_view = self.tmp_satellites_in_view
        self.position_fix_indicator = self.tmp_position_fix_indicator
        self.latitude = self.tmp_latitude
        self.longitude = self.tmp_longitude
        self.antenna_altitude = self.tmp_antenna_altitude
        self.course_over_ground = self.tmp_course_over_ground
        self.speed_over_ground = self.tmp_speed_over_ground

        self.tmp_timestamp = 0.0
        self.tmp_satellites_num = 0
        self.tmp_satellites_in_view = 0        
        self.tmp_position_fix_indicator = 0
        self.tmp_latitude = 0.0
        self.tmp_longitude = 0.0
        self.tmp_antenna_altitude = 0.0
        self.tmp_course_over_ground = 0.0
        self.tmp_speed_over_ground = 0.0
        
    def read_data(self):

        message = ""
        
        if self.uart_dev.inWaiting() > 0:
            logger.debug("good to read")
            data = self.uart_dev.read().decode('ascii')
            if data[0] == self.message_preamble[0]:
                message = data[0]
                while 1:
                    data = self.uart_dev.read().decode('ascii')
                    message += data
                    if data[0] == self.message_postamble[0]:
                        break
        else:
            logger.debug("waiting")
            return -1

        if len(message) == 0:
            logger.debug("empty")
            return -1

        logger.debug(message)
        
        lines = message.split(",")

        if lines[0] == "$GPGGA":
            
            try:
                self.tmp_position_fix_indicator = int(lines[6])
            except:
                logger.debug("GGA issues with position_fix_indicator", lines[6])
                    
            try:
                self.tmp_satellites_num = int(lines[7])
            except:
                logger.debug("GGA issues with satellites_num", lines[7])
                    
            try:
                self.tmp_antenna_altitude = float(lines[9])
            except:
                logger.debug("GGA issues with antenna_altitude", lines[9])

            # all time in sec precision, but millsec possible, just not provided
            #try:
            #    print lines[1]
            #except:
            #    if self.debug:
            #        logger.debug("Getting getting GGA unix_time")
                
        if lines[0] == "$GPGSV":
            try:
                self.tmp_satellites_in_view = int(lines[3])
            except:
                logger.debug("GSV issues with satellites_in_view", lines[3])

        if lines[0] == "$GPRMC":
            
            try:
                self.tmp_latitude = self.geo.Degrees2DecimalDegrees(float(lines[3]))
                if lines[4] == 'S':
                    self.tmp_latitude = -self.tmp_latitude
            except:
                logger.debug("RMC issues with latitude", lines[3], lines[4])

            try:
                self.tmp_longitude = self.geo.Degrees2DecimalDegrees(float(lines[5]))
                if lines[6] == 'W':
                    self.tmp_longitude = -self.tmp_longitude
            except:
                logger.debug("RMC issues with longitude", lines[5], lines[6])

            try:
                self.tmp_speed_over_ground = float(lines[7]) * 0.514444 # m/s
            except:
                logger.debug("RMC issues with speed_over_ground", lines[7])

            try:
                self.tmp_course_over_ground = float(lines[8]) # deg
            except:
                logger.debug("RMC issues with course_over_ground", lines[8])

            # all time in sec precision, but millsec possible, just not provided
            try:
                self.tmp_timestamp = self.convert_datetime_to_unix_timestamp(lines[9], lines[1])
            except:
                logger.debug("RMC issues with utc_time & date", lines[1], lines[9])

        if lines[0] == "$GPVTG":
            self.update()

        return 0
            
    def convert_datetime_to_unix_timestamp(self, nema_date, nema_time):
        if nema_date != "" and nema_time != "":
            d = datetime.datetime(int("20" + nema_date[4:6]), int(nema_date[2:4]), int(nema_date[0:2]),
                                  int(nema_time[0:2]), int(nema_time[2:4]), int(nema_time[4:6]), int(nema_time[7:10]))
            return time.mktime(d.timetuple())
        else:
            return 0.0
