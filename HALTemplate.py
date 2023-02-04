import time
import importlib
from logger_config import logger
from HardwareSettings import HardwareSettings

components = { "1-wire.MAX31850JATB": "My Thermocouple",
               "cam.Cam": "My V4L Camera",               
               "gpio.AccessControl": "My GPIO Access Control",
               "gpio.Buzzer": "My GPIO-based Buzzer",
               "gpio.CXMSeries": "My GPIO-based Oval Gear Flow Sensor",
               "gpio.FanDc": "My DC Fan",
               "gpio.HUB75": "My RGB LED Matrix Display",
               "gpio.StepperMotor": "My Stepper Motor",
               "gpio.Interrupt": "My Interrupt (e.g. Switch, Touch, SW420)",
               "gpio.Light": "My Light",
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

#modules['1-wire.MAX31850JATB'] has no settings?
modules['cam.Cam'].num = HardwareSettings.CAM_NUM
#modules['cam.AccessControl'] WIP
modules['gpio.Buzzer'].pin = HardwareSettings.BUZZER_PIN
modules['gpio.CXMSeries'].pin = HardwareSettings.FLOW_SENSOR_OVAL_GEAR_PIN
modules['gpio.FanDc'].pin = HardwareSettings.FAN_PIN
#modules['gpio.HUB75'] WIP
#modules['gpio.Stepper'] WIP
#modules['gpio.Interrupt'].pin = ?? WIP
modules['gpio.Light'].pin = HardwareSettings.LIGHT_PIN
modules['gpio.YFB7'].pin = HardwareSettings.FLOW_SENSOR_PADDLE_BRASS_PIN
modules['gpio.YFS201'].pin = HardwareSettings.FLOW_SENSOR_PADDLE_PLASTIC_PIN
modules['i2c.DS1775R'].bus = HardwareSettings.TEMP_SENSOR_I2C_BUS
modules['i2c.LTC2497'].bus = HardwareSettings.ADC_I2C_BUS
modules['i2c.MLX90614'].bus = HardwareSettings.TEMP_SENSOR_I2C_BUS
modules['i2c.TSL2591'].bus = HardwareSettings.LIGHT_SENSOR_I2C_BUS
modules['ip.Lpr'].ip_address = HardwareSettings.LPR_IP_ADDRESS
modules['ip.LprMobile'].ip_address = HardwareSettings.LPR_IP_ADDRESS
modules['uart.DR600'].tty = HardwareSettings.RADAR_UART_TTY
modules['uart.DR600'].baudrate = HardwareSettings.RADAR_UART_BAUDRATE
modules['uart.GPSNEMA'].tty = HardwareSettings.GPS_UART_TTY
modules['uart.GPSNEMA'].baudrate = HardwareSettings.GPS_UART_BAUDRATE
modules['uart.RION'].model = HardwareSettings.INCLIOMETER_MODEL
modules['uart.RION'].tty = HardwareSettings.INCLIOMETER_UART_TTY
modules['uart.RION'].baudrate = HardwareSettings.INCLIOMETER_UART_BAUDRATE
modules['uart.Sabertooth'].address = HardwareSettings.MOTOR_CONTROLLER_ADDRESS
modules['uart.Sabertooth'].tty = HardwareSettings.MOTOR_CONTROLLER_UART_TTY
modules['uart.Sabertooth'].baudrate = HardwareSettings.MOTOR_CONTROLLER_UART_BAUDRATE
modules['spi.MAX7301ATL'].bus = HardwareSettings.IO_EXPANDER_SPI_BUS
modules['spi.MAX7301ATL'].device = HardwareSettings.IO_EXPANDER_SPI_DEVICE
modules['spi.MAX7301ATL'].bus_speed = HardwareSettings.IO_EXPANDER_SPI_BUS_SPEED
modules['spi.MCP3008'].bus = HardwareSettings.ADC_SPI_BUS
modules['spi.MCP3008'].device = HardwareSettings.ADC_SPI_DEVICE
modules['spi.MCP3008'].bus_speed = HardwareSettings.ADC_SPI_BUS_SPEED
    
for k, v in modules.items():
    print ("Starting module '%s'" % k)
    v.start()

while 1:

    time.sleep(1)

    for k, v in modules.items():
        logger.info("is_active(%s): %d" % (k, v.is_active))
        
    if modules['gpio.FanDc'].is_active and not modules['gpio.Buzzer'].is_active:
        modules['gpio.Buzzer'].stop()
        modules['gpio.Light'].stop()
