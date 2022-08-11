# coding=utf-8
import RPi.GPIO as GPIO
import pandas as pd
import time
from multiprocessing import Process
import os
import pmsensor_5003 as pmsensor_5003
import pmsensor_sensirion as pmsensor_sensirion
import gps as gps


if __name__ ==  '__main__':
    print("Read and collect data. [Press Ctrl+C to exit!]")
    # GPIO.setmode(GPIO.BCM)

    pmsensor1 = pmsensor_sensirion.PMSensorSensirion()
    sensor = sensor.PMSensor5003()

    # GPIO.setup(rotary.PIN_CLK, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(rotary.PIN_DT, GPIO.IN, pull_up_down = GPIO.PUD_UP)
    # GPIO.setup(rotary.BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # rotary.set_clk_last(GPIO.input(rotary.PIN_CLK))

    # To directly integrate a debounce, the functions for output are initialized by the CallBack-Option of the GPIO Python module
    # GPIO.add_event_detect(rotary.PIN_CLK, GPIO.BOTH, callback=rotary.turn_knob, bouncetime=50)
    # GPIO.add_event_detect(rotary.BUTTON_PIN, GPIO.FALLING, callback=rotary.counter_reset, bouncetime=50)


    try:
        while True:
            pass

    except KeyboardInterrupt:
            GPIO.cleanup()
