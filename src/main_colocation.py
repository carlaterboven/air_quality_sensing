# coding=utf-8
import RPi.GPIO as GPIO
import time
from datetime import datetime
import os
import pmsensor_5003
import pmsensor_7003
import pmsensor_sensirion
import temp_hum_bme680 as humiditysensor
import gassensor_cjmcu6814
import write_data as data_logger

def try_sensor_read(sensor):
    try:
        sensor.read_data()
    except KeyboardInterrupt:
        raise
    except:
        sensor.set_nan_data()

def get_time():
    return {
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

def myloop():
    try:
        print('Read and collect data. [Press Ctrl+C to exit!]')

        pmsensor_sps = pmsensor_sensirion.PMSensorSensirion()
        pmsensor_5003 = pmsensor_5003.PMSensor5003()
        pmsensor_7003 = pmsensor_7003.PMSensor7003()
        temp_hum_sensor = humiditysensor.HumSensor()
        gassensor = gassensor_cjmcu6814.GasSensor()

        file_name = 'log' + str(time.time()) + '.csv'
        datalogger = data_logger.DataLogger('/home/pi/Dokumente/air_quality_sensing/data/' + file_name)

        sensor_list = [pmsensor_sps, pmsensor_5003, pmsensor_7003, temp_hum_sensor, gassensor]

        while True:
            for sensor in sensor_list:
                sensor.reset_data()
            # collect data for 1 minute
            t_end = time.time() + 60
            while time.time() < t_end:
                for sensor in sensor_list:
                    try_sensor_read(sensor)
                time.sleep(1) # measure every second

            data = get_time()
            for sensor in sensor_list:
                data = data | sensor.get_data()
            datalogger.write_data(data)

    except:
        myloop()
        return

myloop()
