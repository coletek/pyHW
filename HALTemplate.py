import time
from logger_config import logger
import importlib

components = { "1-wire.MAX31850JATB": "My Thermocouple",
               "cam.Cam": "My V4L Camera",               
               "gpio.AccessControl": "My GPIO Access Control",
               "gpio.Buzzer": "My GPIO-based Buzzer",
               "gpio.CXMSeries": "My GPIO-based Oval Gear Flow Sensor",
               "gpio.FanDc": "My DC Fan",
               "gpio.HUB75": "My RGB LED Matrix Display",
               "gpio.StepperMotor": "My Stepper Motor",
               "gpio.Interrupt": "My Interrupt (e.g. SW420 or Touch)",
               "gpio.YFB7": "My Brass Paddle Flow Sensor",
               "gpio.YFS201": "My Plastic Paddle Flow Sesnor",
               "i2c.DS1775R": "My i2c-based temp sensor",
               "i2c.LTC2497": "My i2c-based 16ch 16bit delta-sigma ADC",
               "i2c.MLX90614": "My i2c-based temp sensor",
               "i2c.TSL2591": "My light sensor",
               "ip.Lpr": "My IP-based LPR Camera",
               "ip.LprMobile": "My IP-based LPR Mobile Camera",
               "uart.DR600": "My serial-based Radar",
               "uart.GPSNEMA": "My serial-based GPS",
               "uart.RION": "My serial-based incliometer",
               "uart.Sabertooth": "My serial-based dual motor controller",
               "spi.MAX7301ATL": "My spi-based IO expander",
               "spi.MCP3008": "My spi-based 8ch 10bit SAR ADC"
}

modules = {}

for k, v in components.items():
    print ("Loading '%s': %s" % (k, v))
    obj_name = k.split(".")[1]
    module = importlib.import_module(k)
    obj = getattr(module, obj_name)
    modules[k] = obj()

modules['gpio.Buzzer'].pin = 7
modules['gpio.FanDc'].pin = 7
    
for k, v in modules.items():
    print ("Starting module '%s'" % k)
    v.start()

while 1:

    time.sleep(1)

    for k, v in modules.items():
        logger.info("is_active(%s): %d" % (k, v.is_active))
        
    if modules['gpio.FanDc'].is_active and not modules['gpio.Buzzer'].is_active:
        modules['gpio.Buzzer'].stop()
