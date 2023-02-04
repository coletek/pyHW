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

# TODO: upgrade to GPIOController
try:
    import pigpio
except:
    pass

class TSL2591(Device):
    
    # dynamic variables
    
    lux = 0.0
    
    # static variables

    ADDRESS = 0x29
    
    REG_COMMAND_BIT = 0xa0
    
    REG_REGISTER_ENABLE = 0x00
    REG_REGISTER_CONTROL = 0x01
    REG_REGISTER_DEVICE_ID = 0x12
    REG_REGISTER_CHAN0_LOW = 0x14
    REG_REGISTER_CHAN1_LOW = 0x16
    
    REG_ENABLE_POWEROFF = 0x00
    REG_ENABLE_POWERON = 0x01
    REG_ENABLE_AEN = 0x02
    REG_ENABLE_AIEN = 0x10
    REG_ENABLE_NPIEN = 0x80
    
    REG_INTEGRATIONTIME_100MS = 0x00
    REG_INTEGRATIONTIME_200MS = 0x01
    REG_INTEGRATIONTIME_300MS = 0x02
    REG_INTEGRATIONTIME_400MS = 0x03
    REG_INTEGRATIONTIME_500MS = 0x04
    REG_INTEGRATIONTIME_600MS = 0x05
    
    REG_GAIN_LOW = 0x00 # 1x
    REG_GAIN_MED = 0x10 # 25x
    REG_GAIN_HIGH = 0x20 # 428x
    REG_GAIN_MAX = 0x30 # 9876x
    
    REG_LUX_DF = 408 # lux cooefficient
    
    def start(self):
        self.is_active = True
        
        try:
            pigpio.exceptions = True
            self.pi = pigpio.pi()
            self.fd = self.pi.i2c_open(1, self.ADDRESS)
        except:
            logger.debug('no pigpio - assuming simulator')
            self.is_simulator = True

                
    def setup(self):
        if self.is_simulator:
            return
    
        self.integration = self.REG_INTEGRATIONTIME_100MS
        self.gain = self.REG_GAIN_MED
  
        # check ID
        id = self.pi.i2c_read_byte_data(self.fd,
                                        self.REG_COMMAND_BIT |
                                        self.REG_REGISTER_DEVICE_ID)
        if id != 0x50:
            #print ("error: wrong id")
            return -1

        # enable
        self.pi.i2c_write_byte_data(self.fd,
                                    self.REG_COMMAND_BIT |
                                    self.REG_REGISTER_ENABLE,
                                    self.REG_ENABLE_POWERON |
                                    self.REG_ENABLE_AEN |
                                    self.REG_ENABLE_AIEN |
                                    self.REG_ENABLE_NPIEN)

        # set timing and gain
        self.pi.i2c_write_byte_data(self.fd,
                                    self.REG_COMMAND_BIT |
                                    self.REG_REGISTER_CONTROL,
                                    self.integration | self.gain)

        
        # disable
        self.pi.i2c_write_byte_data(self.fd,
                                    self.REG_COMMAND_BIT |
                                    self.REG_REGISTER_ENABLE,
                                    self.REG_ENABLE_POWEROFF)

    def tick(self):
        if self.is_simulator:
            self.lux = random.randrange(0, 100, 1)
            return

        # enable
        self.pi.i2c_write_byte_data(self.fd,
                                    self.REG_COMMAND_BIT |
                                    self.REG_REGISTER_ENABLE,
                                    self.REG_ENABLE_POWERON |
                                    self.REG_ENABLE_AEN |
                                    self.REG_ENABLE_AIEN |
                                    self.REG_ENABLE_NPIEN)
    
        # wait for adc
        time.sleep(1)
    
        y = self.pi.i2c_read_byte_data(self.fd,
                                       self.REG_COMMAND_BIT |
                                       self.REG_REGISTER_CHAN0_LOW)
        x = self.pi.i2c_read_byte_data(self.fd,
                                       self.REG_COMMAND_BIT |
                                       self.REG_REGISTER_CHAN1_LOW)
        
        x <<= 16;
        x |= y;
        lum = x
        
        #print ("full_luminosity=%d" % lum)
        
        ir = lum >> 16
        full = lum & 0xFFFF
        
        #print ("full=%d ir=%d" % (full, ir))
        
        # calculate actual lux value
        # full, ir
        
        if full == 0xffff | ir == 0xffff:
            #print ("error: overflow")
            return -1

        if self.integration == self.REG_INTEGRATIONTIME_100MS:
            atime = 100
        elif self.integration == self.REG_INTEGRATIONTIME_200MS:
            atime = 200
        elif self.integration == self.REG_INTEGRATIONTIME_300MS:
            atime = 300
        elif self.integration == self.REG_INTEGRATIONTIME_400MS:
            atime = 400
        elif self.integration == self.REG_INTEGRATIONTIME_500MS:
            atime = 500
        elif self.integration == self.REG_INTEGRATIONTIME_600MS:
            atime = 600
        else:
            atime = 100
            
        if self.gain == self.REG_GAIN_LOW:
            again = 1
        elif self.gain == self.REG_GAIN_MED:
            again = 25
        elif self.gain == self.REG_GAIN_HIGH:
            again = 428
        elif self.gain == self.REG_GAIN_MAX:
            again = 9876
        else:
            again = 1
            
        cpl = (atime * again) / self.REG_LUX_DF;
        
        if full > 0 and cpl > 0:
            lux = (full - ir) * (1.0 - ir / full) / cpl;
        else:
            lux = 0.0
            
        # disable
        self.pi.i2c_write_byte_data(self.fd,
                                    self.REG_COMMAND_BIT |
                                    self.REG_REGISTER_ENABLE,
                                    self.REG_ENABLE_POWEROFF)
        
        self.lux = lux
