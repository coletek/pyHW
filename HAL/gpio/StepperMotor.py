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

import os
import sys
import time
from logger_config import logger
import GPIOController
import Constants
from Device import Device

try:
    import RPi.GPIO as GPIO # TODO: upgrade to GPIOController
except:
    pass

class StepperMotor(Device):

    # encoder variables

    a_state_previous = 0
    counter = 0

    DIR_CLOCKWISE = 0
    DIR_ANTI_CLOCKWISE = 1

    def setup(self, pin_en, pin_dir, pin_step, pin_a, pin_b, pin_z):
        
        self.pin_en = pin_en
        self.pin_dir = pin_dir
        self.pin_step = pin_step

        self.pin_a = pin_a
        self.pin_b = pin_b
        self.pin_z = pin_z

        try:
        
            GPIO.setmode(GPIO.BCM)

            # setup stepper driver
            
            GPIO.setup(self.pin_en, GPIO.OUT)
            GPIO.setup(self.pin_dir, GPIO.OUT)
            GPIO.setup(self.pin_step, GPIO.OUT)
            GPIO.output(self.pin_en, GPIO.HIGH)
            GPIO.output(self.pin_dir, GPIO.HIGH)
            GPIO.output(self.pin_step, GPIO.HIGH)

            # setup encoder
        
            GPIO.setup(self.pin_a, GPIO.IN)
            GPIO.setup(self.pin_b, GPIO.IN)
            GPIO.setup(self.pin_z, GPIO.IN)
            GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.encoder_tick_callback)

        except:
            logger.debug('no RPi.GPIO - assuming simulator')
            self.is_simulator = True
            
        self.motor_off()
            
    def motor_off(self):
        if not self.is_simulator:
            GPIO.output(self.pin_en, GPIO.HIGH)

    def motor_on(self):
        if not self.is_simulator:
            GPIO.output(self.pin_en, GPIO.LOW)

    def set_motor_direction(self, dir):
        if not self.is_simulator:
            if dir:
                GPIO.output(self.pin_dir, GPIO.HIGH)
            else:
                GPIO.output(self.pin_dir, GPIO.LOW)

    def step_motor(self, speed): # speed in Hz (e.g. 10,000Hz)
        if not self.is_simulator:
            delay = 1.0 / (speed / 2.0)
            GPIO.output(self.pin_step, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(self.pin_step, GPIO.LOW)
            time.sleep(delay)
            
    def motor_move(self, speed, steps): # speed in Hz (e.g. 10,000Hz)
        if not self.is_simulator:
            for x in range(steps):
                step_motor(speed)

    def set_motor_position(self, pos, speed): # speed in Hz (e.g. 10,000Hz)
        if not self.is_simulator:
            if pos > counter:
                self.set_motor_direction(DIR_CLOCKWISE)
                while pos < counter:
                    self.step_motor(speed)
            else:
                self.set_motor_direction(DIR_ANTI_CLOCKWISE)
                while pos > counter:
                    self.step_motor(speed)

    def get_encoder_count(self):
        return self.counter

    def encoder_tick_callback(self):
        if not self.is_simulator:
            a_state = GPIO.input(self.pin_a)

            if (a_state != self.a_state_previous):
                if GPIO.input(self.pin_b) != a_state:
                    self.counter += 1
                else:
                    self.counter -= 1

            logger.debug("ENCODER A=%d B=%d Z=%d counter=%d" % (GPIO.input(self.pin_a), GPIO.input(self.pin_b), GPIO.input(self.pin_z), self.counter))
    
            self.a_state_previous = a_state
