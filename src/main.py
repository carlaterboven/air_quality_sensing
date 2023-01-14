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

def try_sensor_read(sensor):
    try:
        sensor.read_data()
    except KeyboardInterrupt:
        raise
    except:
        sensor.set_nan_data()

def try_gps_read(gps):
    try:
        gps.compute_position()
        if gps.get_data()['lat'] != 'n/a':
            # use green LED to show successfull GPS
            GPIO.output(GREEN_LED, GPIO.HIGH)
        else:
            GPIO.output(GREEN_LED, GPIO.LOW)
    except KeyboardInterrupt:
        raise
    except:
        print('GPS Error')
        GPIO.output(GREEN_LED, GPIO.LOW)


if __name__ ==  '__main__':
    print('Read and collect data. [Press Ctrl+C to exit!]')
    GPIO.setmode(GPIO.BCM)
    RED_LED = 20      # pin for LED to indicate start of measurements and chance to connect usb of gps sensor
    GPIO.setup(RED_LED, GPIO.OUT)
    GPIO.output(RED_LED, GPIO.HIGH)
    GREEN_LED = 21    # pin for LED to indicate successfull gps measurement
    GPIO.setup(GREEN_LED, GPIO.OUT)
    GPIO.output(GREEN_LED, GPIO.LOW)

    print('Please connect GPS sensor via USB.')
    # wait 10 seconds to connect GPS sensor
    time.sleep(10)
    GPIO.output(RED_LED, GPIO.LOW) # gps sensor has to be connected by now

    pmsensor_sps = pmsensor_sensirion.PMSensorSensirion()
    pmsensor_5003 = pmsensor_5003.PMSensor5003()
    pmsensor_7003 = pmsensor_7003.PMSensor7003()
    temp_hum_sensor = humiditysensor.HumSensor()
    gassensor = gassensor_cjmcu6814.GasSensor()
    gps = gps_sensor.Gps()

    file_name = 'log' + str(time.time()) + '.csv'
    datalogger = data_logger.DataLogger('/home/pi/Dokumente/air_quality_sensing/data/' + file_name)

    sensor_list = [pmsensor_sps, pmsensor_5003, pmsensor_7003, temp_hum_sensor]

    try:
        while True:
            for sensor in sensor_list:
                sensor.reset_data()
            # collect data for 3 seconds
            t_end = time.time() + 3
            while time.time() < t_end:
                for sensor in sensor_list:
                    try_sensor_read(sensor)
                time.sleep(1) # measure every second

            try_gps_read(gps)

            data = gps.get_data()
            for sensor in sensor_list:
                data = data | sensor.get_data()
            datalogger.write_data(data)
            #print('write data')

    except KeyboardInterrupt:
            GPIO.output(GREEN_LED, GPIO.LOW)
            GPIO.cleanup()
            pmsensor_7003.__del__()
            pmsensor_sps.__del__()

    except Exception as e:
        file = open('/home/pi/Dokumente/air_quality_sensing/data/errorfile.txt', 'a')
        file.write(e)
        file.write("finished with error")
        file.close()
