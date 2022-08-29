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

    #pmsensor_sps = pmsensor_sensirion.PMSensorSensirion()
    pmsensor_5003 = pmsensor_5003.PMSensor5003()
    pmsensor_7003 = pmsensor_7003.PMSensor7003()
    
    temp_hum_sensor = humiditysensor.HumSensor()

    gps = gps.Gps()
    datalogger = data_logger.DataLogger('../data/log.csv')

    try:
        while True:
            #pmsensor_sps.reset_data()
            pmsensor_5003.reset_data()
            pmsensor_7003.reset_data()
            temp_hum_sensor.reset_data()
            # collect data for 5 seconds
            t_end = time.time() + 5
            while time.time() < t_end:
                #pmsensor_sps.read_data()
                pmsensor_5003.read_data()
                pmsensor_7003.read_data()
                temp_hum_sensor.read_data()
            #print(pmsensor_sps.get_data())
            #print(pmsensor_5003.get_data())
            #print(pmsensor_7003.get_data())
            #print(temp_hum_sensor.get_data())
            gps.compute_position()
            #datalogger.write_data(gps.get_data() | pmsensor_sps.get_data() | pmsensor_5003.get_data() | pmsensor_7003.get_data() | temp_hum_sensor.get_data())
            datalogger.write_data(gps.get_data() | pmsensor_5003.get_data() | pmsensor_7003.get_data() | temp_hum_sensor.get_data())

    except KeyboardInterrupt:
            GPIO.cleanup()
            pmsensor_7003.__del__()
            #pmsensor_sps.__del__()
