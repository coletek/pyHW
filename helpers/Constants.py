class Constants:

    PWM_LED = 100
    PWM_MOTOR = 4000 # or higher for brushed DC motors
    PWM_BUZZER = 2500 # common

    CXM_SERIES_LITRES_PER_PULSE = 0.017637 # http://www.gninstruments.com/english/html/83-2/2377.htm
    YFS201_LITRES_PER_PULSE = 1.0 / 450.0 # https://www.adafruit.com/product/828
    YFB7_FLOW_RATE_TO_FREQ = 11.0 # https://www.robotshop.com/en/water-flow-sensor-yf-b7.html
