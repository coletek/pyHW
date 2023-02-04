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
    modules[k] = importlib.import_module(k)

# TODO
theromocuple = modules['1-wire.MAX31850JATB'].MAX31850JATB()
cam = modules['cam.Cam'].Cam()
access_control = modules['gpio.AccessControl'].AccessControl()

buzzer = modules['gpio.Buzzer'].Buzzer()
buzzer.pin = 7
buzzer.start()

# TODO
flow_sensor_oval_gear = modules['gpio.CXMSeries'].CXMSeries()

fan = modules['gpio.FanDc'].FanDc()
fan.pin = 7
fan.start()

# TODO
matrix_display = modules['gpio.HUB75'].HUB75()
stepper_motor = modules['gpio.StepperMotor'].StepperMotor()
interrupt = modules['gpio.Interrupt'].Interrupt()
flow_sensor_paddle_brass = modules['gpio.YFB7'].YFB7()
flow_sensor_paddle_plastic = modules['gpio.YFS201'].YFS201()
temp_sensor = modules['i2c.DS1775R'].DS1775R()
adc_16ch_16bit_deltasigma = modules['i2c.LTC2497'].LTC2497()
temp_sensor2 = modules['i2c.MLX90614'].MLX90614()
light_sensor = modules['i2c.TSL2591'].TSL2591()
lpr = modules['ip.Lpr'].Lpr()
lpr_mobile = modules['ip.LprMobile'].LprMobile()
radar_sensor = modules['uart.DR600'].DR600()
gps_sensor = modules['uart.GPSNEMA'].GPSNEMA()
inclinometer_sensor = modules['uart.RION'].RION()
motor_controller = modules['uart.Sabertooth'].Sabertooth()
io_expander = modules['spi.MAX7301ATL'].MAX7301ATL()
adc_8ch_10bit_sar = modules['spi.MAX7301ATL'].MAX7301ATL()

while 1:

    time.sleep(1)
    logger.info("==== STATUS ====\n"
                "simple gpio: buzzer=%d fan=%d interrupt=%d io_expander=%d\n"
                "flow sensors: paddle_plastic=%d paddle_brass=%d oval_gear=%d\n"
                "motor ctrls: stepper=%d sabertooth=%d\n"
                "temp sensors: DS1775R=%d MLX90614=%d\n"
                "cams: V4L=%d LPR=%d LPR_MOBILE=%d\n"
                "ADCs: LTC2497=%d MCP3008=%d\n"
                "Other Sensors: light=%d radar=%d gps=%d inclinometer=%d" %
                (buzzer.is_active, fan.is_active, interrupt.is_active, io_expander.is_active,
                 flow_sensor_paddle_plastic.is_active, flow_sensor_paddle_brass.is_active, flow_sensor_oval_gear.is_active,
                 stepper_motor.is_active, motor_controller.is_active,
                 temp_sensor.is_active, temp_sensor2.is_active,
                 cam.is_active, lpr.is_active, lpr_mobile.is_active,
                 adc_16ch_16bit_deltasigma.is_active, adc_8ch_10bit_sar.is_active,
                 light_sensor.is_active, radar_sensor.is_active, gps_sensor.is_active, inclinometer_sensor.is_active))

    if fan.is_active and not buzzer.is_active:
        fan.stop()
