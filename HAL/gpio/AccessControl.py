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

# TODO: upgrade to GPIOController
import time
try:
    import RPi.GPIO as GPIO
except:
    pass

class AccessControl(Device):

    NOT_UP_OR_DOWN = -1
    DOWN = 0
    UP = 1
    
    def setup(self,
              entry_power = 2, # not implemented yet
              entry_leds = 3, # not implemented yet
              entry_ctrl_stop = 4, entry_ctrl_down = 5, entry_ctrl_up = 6,
              entry_status_down = 7, entry_status_up = 8,
              entry_status_loop_open = 9, entry_status_loop_close_before = 10, entry_status_loop_close_after = 11,
              entry_status_ir = 12,
            
              buzzer = 13,
              pdis = 16,  # power isolation enable/disable pin
              
              exit_power = 17, # not implemented yet
              exit_leds = 18, # not implemented yet
              exit_ctrl_stop = 19, exit_ctrl_down = 20, exit_ctrl_up = 21,
              exit_status_down = 22, exit_status_up = 23,
              exit_status_loop_open = 24, exit_status_loop_close_before = 25, exit_status_loop_close_after = 26,
              exit_status_ir = 27):
        
        self.pin_gate_entry_ctrl_stop = entry_ctrl_stop
        self.pin_gate_entry_ctrl_down = entry_ctrl_down
        self.pin_gate_entry_ctrl_up = entry_ctrl_up
        self.pin_gate_entry_status_down = entry_status_down
        self.pin_gate_entry_status_up = entry_status_up
        self.pin_gate_entry_status_loop_open = entry_status_loop_open
        self.pin_gate_entry_status_loop_close_before = entry_status_loop_close_before
        self.pin_gate_entry_status_loop_close_after = entry_status_loop_close_after
        self.pin_gate_entry_status_ir = entry_status_ir
        self.pin_buzzer = buzzer
        self.pin_pdis = pdis       
        self.pin_gate_exit_ctrl_stop = exit_ctrl_stop
        self.pin_gate_exit_ctrl_up = exit_ctrl_up
        self.pin_gate_exit_ctrl_down = exit_ctrl_down
        self.pin_gate_exit_status_up = exit_status_up
        self.pin_gate_exit_status_down = exit_status_down
        self.pin_gate_exit_status_loop_open = exit_status_loop_open
        self.pin_gate_exit_status_loop_close_before = exit_status_loop_close_before
        self.pin_gate_exit_status_loop_close_after = exit_status_loop_close_after
        self.pin_gate_exit_status_ir = exit_status_ir

        try:

            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)

            GPIO.setup(self.pin_pdis, GPIO.OUT)
            GPIO.output(self.pin_pdis, GPIO.LOW) # enable power isolation

            GPIO.setup(self.pin_buzzer, GPIO.OUT)
            self.buzzer_pwm = GPIO.PWM(self.pin_buzzer, 3000)
            
            GPIO.setup(self.pin_gate_entry_ctrl_stop, GPIO.OUT)
            GPIO.setup(self.pin_gate_entry_ctrl_down, GPIO.OUT)
            GPIO.setup(self.pin_gate_entry_ctrl_up, GPIO.OUT)
            GPIO.setup(self.pin_gate_entry_status_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_entry_status_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_entry_status_loop_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_entry_status_loop_close_before, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_entry_status_loop_close_after, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_entry_status_ir, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            
            GPIO.setup(self.pin_gate_exit_ctrl_stop, GPIO.OUT)
            GPIO.setup(self.pin_gate_exit_ctrl_down, GPIO.OUT)
            GPIO.setup(self.pin_gate_exit_ctrl_up, GPIO.OUT)
            GPIO.setup(self.pin_gate_exit_status_down, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_exit_status_up, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_exit_status_loop_open, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_exit_status_loop_close_before, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_exit_status_loop_close_after, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(self.pin_gate_exit_status_ir, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.output(self.pin_gate_entry_ctrl_stop, GPIO.LOW)
            GPIO.output(self.pin_gate_entry_ctrl_down, GPIO.LOW)
            GPIO.output(self.pin_gate_entry_ctrl_up, GPIO.LOW)
            
            GPIO.output(self.pin_gate_exit_ctrl_stop, GPIO.LOW)
            GPIO.output(self.pin_gate_exit_ctrl_down, GPIO.LOW)        
            GPIO.output(self.pin_gate_exit_ctrl_up, GPIO.LOW)

        except:
            logger.debug('no RPi.GPIO - assuming simulator')
            self.is_simulator = True

    def speaker_on(self):
        if self.is_simulator:
            logger.debug("s")
            return
        self.buzzer_pwm.start(50)
            
    def speaker_off(self):
        if self.is_simulator:
            logger.debug("s")
            return
        self.buzzer_pwm.stop()
                    
    # to trigger output - set high, wait for at least 20ms, set low again
            
    def gate_entry_stop(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_entry_ctrl_stop, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_entry_ctrl_stop, GPIO.LOW)
            time.sleep(2) # required if we are stopping when gate is coming down
        
    def gate_entry_down(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_entry_ctrl_up, GPIO.LOW)
            GPIO.output(self.pin_gate_entry_ctrl_down, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_entry_ctrl_down, GPIO.LOW)

    def gate_entry_up(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_entry_ctrl_down, GPIO.LOW)
            GPIO.output(self.pin_gate_entry_ctrl_up, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_entry_ctrl_up, GPIO.LOW)

    def gate_exit_stop(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_exit_ctrl_stop, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_exit_ctrl_stop, GPIO.LOW)
            time.sleep(2) # required if we are stopping when gate is coming down

    def gate_exit_down(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_exit_ctrl_up, GPIO.LOW)
            GPIO.output(self.pin_gate_exit_ctrl_down, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_exit_ctrl_down, GPIO.LOW)

    def gate_exit_up(self):
        if not self.is_simulator:
            GPIO.output(self.pin_gate_exit_ctrl_down, GPIO.LOW)
            GPIO.output(self.pin_gate_exit_ctrl_up, GPIO.HIGH)
            time.sleep(0.02)
            GPIO.output(self.pin_gate_exit_ctrl_up, GPIO.LOW)

    def get_gate_entry_position(self):

        if not self.is_simulator:

            if not GPIO.input(self.pin_gate_entry_status_down) and \
               not GPIO.input(self.pin_gate_entry_status_up):
                return self.NOT_UP_OR_DOWN
            
            if not GPIO.input(self.pin_gate_entry_status_down):
                return self.UP
            
            if not GPIO.input(self.pin_gate_entry_status_up):
                return self.DOWN
            
        return self.NOT_UP_OR_DOWN

    def get_gate_exit_position(self):

        if not self.is_simulator:

            if not GPIO.input(self.pin_gate_exit_status_down) and \
               not GPIO.input(self.pin_gate_exit_status_up):
                return self.NOT_UP_OR_DOWN
            
            if not GPIO.input(self.pin_gate_exit_status_down):
                return self.UP
        
            if not GPIO.input(self.pin_gate_exit_status_up):
                return self.DOWN
        
        return self.NOT_UP_OR_DOWN

    # typically not used
    def is_gate_entry_loop_open_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_entry_status_loop_open):
                return True
        return False

    def is_gate_entry_loop_close_before_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_entry_status_loop_close_before):
                return True
        return False

    def is_gate_entry_loop_close_after_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_entry_status_loop_close_after):
                return True
        return False
    
    def is_gate_entry_ir_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_entry_status_ir):
                return True
        return False
    
    def is_gate_exit_loop_open_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_exit_status_loop_open):
                return True
        return False
    
    def is_gate_exit_loop_close_before_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_exit_status_loop_close_before):
                return True
        return False

    def is_gate_exit_loop_close_after_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_exit_status_loop_close_after):
                return True
        return False

    def is_gate_exit_ir_active(self):

        if not self.is_simulator:
            if GPIO.input(self.pin_gate_exit_status_ir):
                return True
        return False
    
