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

"""
MLX90614 driver. 
You might need to enter this command on your Raspberry Pi:
echo "Y" > /sys/module/i2c_bcm2708/parameters/combined
(I've put it in my rc.local so it's executed each bootup)
"""

from logger_config import logger
import GPIOController
from Constants import Constants
from Device import Device

# TODO: upgrade to GPIOController
from time import sleep
try:
    import smbus
except:
    pass

class MLX90614(Device):

    bus_num = 1
    address = 0x5a
    
    MLX90614_RAWIR1=0x04
    MLX90614_RAWIR2=0x05
    MLX90614_TA=0x06
    MLX90614_TOBJ1=0x07
    MLX90614_TOBJ2=0x08

    MLX90614_TOMAX=0x20
    MLX90614_TOMIN=0x21
    MLX90614_PWMCTRL=0x22
    MLX90614_TARANGE=0x23
    MLX90614_EMISS=0x24
    MLX90614_CONFIG=0x25
    MLX90614_ADDR=0x0E
    MLX90614_ID1=0x3C
    MLX90614_ID2=0x3D
    MLX90614_ID3=0x3E
    MLX90614_ID4=0x3F

    comm_retries = 5
    comm_sleep_amount = 0.1

    def start(self):
        self.is_active = True
        
        try:
            self.bus = smbus.SMBus(bus=bus_num)
        except:
            logger.debug('no SMBus - assuming simulator')
            self.is_simulator = True

    def read_reg(self, reg_addr):
        if self.is_simulator:
            return
        
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                #"Rate limiting" - sleeping to prevent problems with sensor 
                #when requesting data too quickly
                sleep(self.comm_sleep_amount)
        #By this time, we made a couple requests and the sensor didn't respond
        #(judging by the fact we haven't returned from this function yet)
        #So let's just re-raise the last IOError we got
        raise e

    def data_to_temp(self, data):
        temp = (data*0.02) - 273.15
        return temp

    def get_amb_temp(self):
        if self.is_simulator:
            return
        data = self.read_reg(self.MLX90614_TA)
        return self.data_to_temp(data)

    def get_obj_temp(self):
        if self.is_simulator:
            return
        data = self.read_reg(self.MLX90614_TOBJ1)
        return self.data_to_temp(data)


if __name__ == "__main__":
    sensor = MLX90614()
    print(sensor.get_amb_temp())
    print(sensor.get_obj_temp())
