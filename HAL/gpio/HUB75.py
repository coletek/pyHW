# pyHW
# Copyright (C) 2022-2023 Luke Cole
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

# TODO: upgrade to GPIOController maybe...
import time
from PIL import Image
try:
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
except:
    pass

class HUB75(Device):
    
    def start(self):
        self.is_active = True
        
        try:
            # Configuration for the matrix
            options = RGBMatrixOptions()
            
            # core features to make it work
            options.brightness = 100
            options.chain_length = 6
            options.cols = 64
            options.rows = 64
            options.disable_hardware_pulsing = True
            options.hardware_mapping = "adafruit-hat-pwm"
            options.multiplexing = 1
            options.parallel = 1
            options.pixel_mapper_config = "U-mapper"
            options.gpio_slowdown = 4
            
            # more settings - helps a bit
            options.inverse_colors = False
            options.led_rgb_sequence = "RGB"
            options.limit_refresh_rate_hz = 0
            #options.panel_type = None
            options.pwm_bits = 4 #11 best for max colours, but increases flicker
            options.pwm_dither_bits = 2
            options.pwm_lsb_nanoseconds = 300
            options.row_address_type = 0
            options.scan_mode = 0
            options.show_refresh_rate = False
            
            self.matrix = RGBMatrix(options = options)
        except:
            logger.debug("no pigpio - assuming simulator")
            self.is_simulator = True
            
    def set_brightness(self, brightness):
        logger.debug("brightness=%d" % brightness)
        if self.is_simulator:
            return
    
        self.matrix.brightness = brightness
              
    def setup_canvas(self):
        logger.debug("")
        if self.is_simulator:
            return
        
        self.canvas = self.matrix.CreateFrameCanvas()
        self.canvas.Clear()
        time.sleep(2)

    def set_scrolling_text(self, y, text):
        logger.debug("set_scrolling_text(%d, %s)" % (y, text))
        if self.is_simulator:
            return

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./rpi-rgb-led-matrix/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width

        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, y, textColor, text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

    def set_text(self, x, y, text):
        logger.debug("set_text(%d, %d, %s)" % (x, y, text))
        if self.is_simulator:
            return

        font = graphics.Font()
        font.LoadFont("./rpi-rgb-led-matrix/fonts/7x13.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = self.canvas.width
    
        len = graphics.DrawText(self.canvas, font, x, y, textColor, text)
        pos -= 1
        if (pos + len < 0):
            pos = self.canvas.width
        time.sleep(0.05)

    def write_canvas(self):
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def clear(self):
        logger.debug("clear()")
        if self.is_simulator:
            return
        self.matrix.Clear()
      
    def set_image(self, image):
        logger.debug("set_image()")
        if self.is_simulator:
            return

        logger.debug("set_image(%s)" % image)
    
        image.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
            
        self.matrix.SetImage(image.convert('RGB'))
    
