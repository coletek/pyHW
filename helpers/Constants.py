class Constants:

    FREQ_LED = 100
    FREQ_MOTOR = 4000
    FREQ_MOTOR_DC_BRUSHED = 20000
    FREQ_BUZZER = 2500 # common

    LM335_SCALE = 0.01 # 10mV/K
    KELVIN_TO_DEGREE = -273.15

    # based on using MCP3008 with MCP1541
    ADC_VREF = 4.096
    ADC_BITS = 1023.0
    
    CXM_SERIES_LITRES_PER_PULSE = 0.017637 # http://www.gninstruments.com/english/html/83-2/2377.htm
    YFS201_LITRES_PER_PULSE = 1.0 / 450.0 # https://www.adafruit.com/product/828
    YFB7_FLOW_RATE_TO_FREQ = 11.0 # https://www.robotshop.com/en/water-flow-sensor-yf-b7.html
