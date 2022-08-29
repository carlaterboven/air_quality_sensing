# coding=utf-8
import RPi.GPIO as GPIO
#import pandas as pd
import time
#from multiprocessing import Process
import os
import gps
import pmsensor_5003
import pmsensor_7003
import pmsensor_sensirion
import temp_hum_bme680 as humiditysensor
import gassensor_cjmcu6814 as gassensor
import write_data as data_logger


if __name__ ==  '__main__':
    print("Read and collect data. [Press Ctrl+C to exit!]")
    GPIO.setmode(GPIO.BCM)

#    pmsensor = pmsensor_sensirion.PMSensorSensirion()
    pmsensor = pmsensor_5003.PMSensor5003()

#    GPIO.setup(pmsensor.GPIO_RX, GPIO.IN)
#    GPIO.setup(pmsensor.GPIO_TX, GPIO.OUT)
    # GPIO.setup(rotary.BUTTON_PIN, GPIO.IN, pull_up_down = GPIO.PUD_UP)

    # rotary.set_clk_last(GPIO.input(rotary.PIN_CLK))

    # To directly integrate a debounce, the functions for output are initialized by the CallBack-Option of the GPIO Python module
    # GPIO.add_event_detect(rotary.PIN_CLK, GPIO.BOTH, callback=rotary.turn_knob, bouncetime=50)
    # GPIO.add_event_detect(rotary.BUTTON_PIN, GPIO.FALLING, callback=rotary.counter_reset, bouncetime=50)

    gps = gps.Gps()
    datalogger = data_logger.DataLogger('../data/log.csv')

    try:
        while True:
            pmsensor.read_data()
            time.sleep(5)
            pmsensor.prepare_data()
            print(pmsensor.get_data())
            gps.compute_position()
            print(gps.get_data())
            datalogger.write_data(gps.get_data(), pmsensor.get_data())

    except KeyboardInterrupt:
            GPIO.cleanup()
