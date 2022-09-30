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
import gassensor_cjmcu6814
import write_data as data_logger


if __name__ ==  '__main__':
    print("Read and collect data. [Press Ctrl+C to exit!]")
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(21, GPIO.OUT) # pin for LED to indicate successfull measurement
    GPIO.output(21, GPIO.LOW)
    
    print("Please connect GPS sensor via USB.")
    # wait 10 seconds to connect GPS sensor
    time.sleep(10)

    #pmsensor_sps = pmsensor_sensirion.PMSensorSensirion()
    pmsensor_5003 = pmsensor_5003.PMSensor5003()
    pmsensor_7003 = pmsensor_7003.PMSensor7003()
    
    temp_hum_sensor = humiditysensor.HumSensor()
    gassensor = gassensor_cjmcu6814.GasSensor()

    gps = gps.Gps()
    file_name = 'log' + str(time.time()) + '.csv'
    datalogger = data_logger.DataLogger('/home/pi/Dokumente/air_quality_sensing/data/' + file_name)

    try:
        while True:
            #pmsensor_sps.reset_data()
            pmsensor_5003.reset_data()
            pmsensor_7003.reset_data()
            temp_hum_sensor.reset_data()
            gassensor.reset_data()
            # collect data for 3 seconds
            t_end = time.time() + 3
            while time.time() < t_end:
                #pmsensor_sps.read_data()
                pmsensor_5003.read_data()
                pmsensor_7003.read_data()
                temp_hum_sensor.read_data()
                gassensor.read_data()
                time.sleep(1) # measure every second
            #print(pmsensor_sps.get_data())
            #print(pmsensor_5003.get_data())
            #print(pmsensor_7003.get_data())
            #print(temp_hum_sensor.get_data())
            #print(gassensor.get_data())
            try:
                gps.compute_position()
                if gps.get_data()['lat'] != 'n/a':
                    # use LED to show successfull GPS
                    GPIO.output(21, GPIO.HIGH)
            except ConnectionResetError:
                print('ConnectionResetError')
            #datalogger.write_data(gps.get_data() | pmsensor_sps.get_data() | pmsensor_5003.get_data() | pmsensor_7003.get_data() | temp_hum_sensor.get_data() | gassensor.get_data())
            datalogger.write_data(gps.get_data() | pmsensor_5003.get_data() | pmsensor_7003.get_data() | temp_hum_sensor.get_data() | gassensor.get_data())

    except KeyboardInterrupt:
            GPIO.cleanup()
            pmsensor_7003.__del__()
            #pmsensor_sps.__del__()
