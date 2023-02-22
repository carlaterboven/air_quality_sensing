# coding=utf-8
import RPi.GPIO as GPIO
import time
import os
import gps_sensor
import pmsensor_5003
import pmsensor_7003
import pmsensor_sensirion
import temp_hum_bme680 as humiditysensor
import write_data as data_logger
import sys
sys.path.append('../../simulated_scripted_exposure_study/src')
from sonification import *

        
class RealTimeSonification():
    def __init__(self, sampling_time):
        self.__pmsensor_sps = pmsensor_sensirion.PMSensorSensirion()
        self.__pmsensor_5003 = pmsensor_5003.PMSensor5003()
        self.__pmsensor_7003 = pmsensor_7003.PMSensor7003()
        self.__temp_hum_sensor = humiditysensor.HumSensor()
        self.__gps = gps_sensor.Gps()
        
        self.__sampling_time = sampling_time
        self.__sonification_logic = SonificationLogic(self.__sampling_time)

        self.__file_name = 'log' + str(time.time()) + '.csv'
        self.__datalogger = data_logger.DataLogger('/home/pi/Dokumente/air_quality_sensing/data/' + self.__file_name)

        self.__sensor_list = [self.__pmsensor_sps, self.__pmsensor_5003, self.__pmsensor_7003, self.__temp_hum_sensor]
        self.__current_data = {}
        self.__pm25_model = {'intercept': 236.811578,
                                'Temperature': -0.8362344519399749,
                                'Relative_Humidity': -0.2450215855176837,
                                'Pressure': -0.20451594934190478,
                                'adjusted_7003_nc1': -24.078732881769838,
                                'adjusted_7003_nc2.5': 24.40651305536212,
                                'SPS_nc1': -0.2001422164432161,
                                'SPS_nc2.5': 0.1448523455040038}
        self.__pm10_model = {'intercept': 198.428905,
                                'Temperature': -0.14278992737700533,
                                'Relative_Humidity': -0.34871100871820576,
                                'Pressure': -0.16117068286679956,
                                'adjusted_7003_nc5': -165.22398021677273,
                                'adjusted_7003_nc10': 165.40755230000087,
                                'SPS_nc4': -8.278088841232316,
                                'SPS_nc10': 8.298401220613906}


    def __del__(self):
        self.__pmsensor_7003.__del__()
        self.__pmsensor_sps.__del__()
    
    def try_sensor_read(self, sensor):
        try:
            sensor.read_data()
        except KeyboardInterrupt:
            raise
        except:
            sensor.set_nan_data()
    
    def read_and_write_data(self):
        for sensor in self.__sensor_list:
            sensor.reset_data()
        # collect data as long as sampling time is chosen (substract 0.5 to hear sound without interruptions)
        t_end = time.time() + self.__sampling_time - 0.3
        while time.time() < t_end:
            for sensor in self.__sensor_list:
                self.try_sensor_read(sensor)
            time.sleep(1) # measure every second
        data = self.__gps.get_data()
        for sensor in self.__sensor_list:
            data = data | sensor.get_data()
        self.__current_data = data
        self.__datalogger.write_data(data)
        #print('write data')
        
    def level_bme680(self):
        self.__current_data['Relative_Humidity'] = self.__current_data['Relative_Humidity'] + 8
        self.__current_data['Temperature'] = self.__current_data['Temperature'] - 4
        
    def adjust_nc_7003(self):
        self.__current_data['adjusted_7003_nc0.5'] = (self.__current_data['7003_nc0.3'] + self.__current_data['7003_nc0.5'])
        self.__current_data['adjusted_7003_nc1'] = (self.__current_data['adjusted_7003_nc0.5'] + self.__current_data['7003_nc1'])
        self.__current_data['adjusted_7003_nc2.5'] = (self.__current_data['adjusted_7003_nc1'] + self.__current_data['7003_nc2.5'])
        self.__current_data['adjusted_7003_nc5'] = (self.__current_data['adjusted_7003_nc2.5'] + self.__current_data['7003_nc5'])
        self.__current_data['adjusted_7003_nc10'] = (self.__current_data['adjusted_7003_nc5'] + self.__current_data['7003_nc10'])
        self.__current_data['adjusted_7003_nc0.3'] = self.__current_data['7003_nc0.3'] / 100
        self.__current_data['adjusted_7003_nc0.5'] = self.__current_data['adjusted_7003_nc0.5'] / 100
        self.__current_data['adjusted_7003_nc1'] = self.__current_data['adjusted_7003_nc1'] / 100
        self.__current_data['adjusted_7003_nc2.5'] = self.__current_data['adjusted_7003_nc2.5'] / 100
        self.__current_data['adjusted_7003_nc5'] = self.__current_data['adjusted_7003_nc5'] / 100
        self.__current_data['adjusted_7003_nc10'] = self.__current_data['adjusted_7003_nc10'] / 100
        
    def calibrate_pm25(self):
        self.__current_data['intercept'] = 1
        pm25 = 0
        for parameter in self.__pm25_model.keys():
            pm25 = pm25 + self.__pm25_model[parameter] * self.__current_data[parameter]
        if pm25 < 0:
            pm25 = 0.0
        return pm25

    def calibrate_pm10(self):
        self.__current_data['intercept'] = 1
        pm10 = 0
        for parameter in self.__pm10_model.keys():
            pm10 = pm10 + self.__pm10_model[parameter] * self.__current_data[parameter]
        if pm10 < 0:
            pm10 = 0.0
        return pm10
        
    def sonify(self):
        self.read_and_write_data()
        self.level_bme680()
        self.adjust_nc_7003()
        # TODO treat outliers
        pm25 = self.calibrate_pm25()
        pm10 = self.calibrate_pm10()
        self.play_sound(pm25, pm10)
        
    def play_sound(self, pm25, pm10):
        position = 4
        self.__sonification_logic.play_sound(pm25, pm10)
        print('position, pm2.5, pm10: ', position, pm25, pm10)        
        


if __name__ ==  '__main__':
    print('Read and collect data. [Press Ctrl+C to exit!]')

    print('Please connect GPS sensor via USB.')
    # wait 10 seconds to connect GPS sensor
    #time.sleep(10)
        
    sampling_time = 2 # measure every 2 seconds
    realtimesony = RealTimeSonification(sampling_time)

    try:
        while True:
            realtimesony.sonify()

    except KeyboardInterrupt:
            realtimesony.__del__()

    except Exception as e:
        file = open('/home/pi/Dokumente/air_quality_sensing/data/errorfile.txt', 'a')
        file.write(str(e))
        file.write("finished with error")
        file.close()
