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

# https://www.alchemy-power.com/wp-content/uploads/2017/03/Pi-16ADC-User-Guide.pdf
# https://github.com/gilmedel/Pi-16ADC/blob/master/pi16adc_test.py
# 6.4s cycle time when reading all data with 0.2s delay between ch

from logger_config import logger
import GPIOController
from Constants import Constants
from Device import Device

# TODO: upgrade to GPIOController
try:
    import pigpio
except:
    pass

class LTC2497(Device):

    VREF = 5.0
    MAX_READING = 8388608.0
    DELAY_AFTER_WRITE = 0.2
    DELAY_BETWEEN_READS = 0.2
    BYTE_BLOCK_SIZE = 0x06 # number of bytes to read in the block
    ADDRESS = 0x14

    MAPPING = {
        0xB0: "BL_MOTOR_IS_A",
        0xB8: "BL_MOTOR_IS_B",
        0xB1: "BR_MOTOR_IS_A",
        0xB9: "BR_MOTOR_IS_B",
        0xB2: "FL_MOTOR_IS_A",
        0xBA: "FL_MOTOR_IS_B",
        0xB3: "FR_MOTOR_IS_A",
        0xBB: "FR_MOTOR_IS_B",
        0xB4: "BL_DISTANCE_SENSOR",
        0xBC: "BR_DISTANCE_SENSOR",
        0xB5: "FL_DISTANCE_SENSOR",
        0xBD: "FR_DISTANCE_SENSOR",
        0xB6: "THERMISTOR0",
        0xBE: "THERMISTOR1",
        0xB7: "THERMISTOR2",
        0xBF: "MOTORS_CURRENT_SENSOR",
    }
    
    DATA = {
        "BL_MOTOR_IS_A": -1,
        "BL_MOTOR_IS_B": -1,
        "BR_MOTOR_IS_A": -1,
        "BR_MOTOR_IS_B": -1,
        "FL_MOTOR_IS_A": -1,
        "FL_MOTOR_IS_B": -1,
        "RF_MOTOR_IS_A": -1,
        "RF_MOTOR_IS_B": -1,
    
        "BL_DISTANCE_SENSOR": -1,
        "BR_DISTANCE_SENSOR": -1,
        "FL_DISTANCE_SENSOR": -1,
        "FR_DISTANCE_SENSOR": -1,
        
        "THERMISTOR0": -1,
        "THERMISTOR1": -1,
        "THERMISTOR2": -1,
        
        "MOTORS_CURRENT_SENSOR": -1,
    }
        
    def start(self):
        self.is_active = True

        try:
            pigpio.exceptions = True
            self.pi = pigpio.pi()
            self.h = self.pi.i2c_open(1, self.ADDRESS)
        except:
            logger.debug('no RPi.GPIO - assuming simulator')
            self.is_simulator = True

    def read(self, channels):
    
        i = 0
        for ch in channels:
            try:
                self.pi.i2c_write_byte(self.h, ch)
            except:
                logger.debug("ch[%d]: i2c write byte error" % i)
            else:
                time.sleep(self.DELAY_AFTER_WRITE)
                (b, d) = self.pi.i2c_read_i2c_block_data(self.h, ch, self.BYTE_BLOCK_SIZE)
                if b >= 0:
                    reading = d
                    if (reading[0] & 0b11000000) == 0b11000000:
                        logger.debug("ch[%d]: error response" % i)
                    else:
                        valor = ((((reading[0]&0x3F))<<16))+((reading[1]<<8))+(((reading[2]&0xE0)))
                        volts = valor * self.VREF / self.MAX_READING
                        name = self.MAPPING[ch]
                        self.DATA[name] = volts
                        logger.debug("ch[%d]: %fV" % (i, volts))
                else:
                    logger.debug("ch[%d]: i2c read block error" % i)
                    pass
         
            time.sleep(self.DELAY_BETWEEN_READS)
            i += 1

    def motor_current(self, V_is):
        # NOTE: doesn't work - PCB design error - needs a AC to DC converter in the loop, or faster ADC

        # pg16 - https://www.infineon.com/dgdl/Infineon-IFX007T-DS-v01_00-EN.pdf?fileId=5546d46265f064ff0166433484070b75
            
        I_is_offset = 0.000170
        d_k_ilis = 19.5e3
        I_is_lim = 0.005
        R_is = 390
        
        I_is = V_is / R_is
        I = d_k_ilis * (I_is - I_is_offset)
        
        if I_is < I_is_offset:
            return 0
        
        if I_is > I_is_lim:
            return -1
        
        return I

    def distance_sensor(self, V):
        # TODO
        
        return V

    def temp_sensor(self, V):
        # NOTE: UNTESTED

        r1 = 4300
        r2 = 1500
        vf = self.VREF
        vo = V
        rt = 1 / ((vf - vo) / (vo * r1) - 1 / r2) # voltage divider
        k = 273.15 # Kelvin conversion
        beta = 3380.0 # b-contant - see datasheet
        temp_0 = 25.0 + k # Kelvin at room temp
        r_0 = 10000.0 # Resistance at room temp
        actual = 1 / (1 / temp_0 + (1 / beta) * math.log(rt / r_0)) - k # Steinhart-Hart approximation
        return actual

    def current_sensor(self, V):
        # NOTE: doesn't work - PCB design error - needs a AC to DC converter in the loop, or faster ADC

        # https://vacuumschmelze.com/Assets-Web/4647-X662.pdf
        
        Rref = 10
        Rin = 10e3
        gain = 1 + Rref / Rin
        Rsense = 680 # I don't think this is correct, it's Rm, which is undefined
        
        return V/gain/Rsense
