from sps30 import SPS30
from time import sleep
import pmsensor

class PMSensorSensirion(pmsensor.PMSensor):

    def __init__(self):
        super().__init__()
        self.__sps = SPS30(3) # 1 when temp_hum_sensor not connected, else 3
        self.__sps.start_measurement()
        sleep(2) # seems to be necessary for I2C bus
        
    def __del__(self):
        self.__sps.stop_measurement()
        sleep(2) # seems to be necessary for I2C bus
        self.__sps.start_fan_cleaning() # enables fan-cleaning manually for 10 seconds (referred by datasheet)
    
    def get_data(self):
        self.prepare_data()
        return {
            'SPS_PM1': self.get_pm1(),
            'SPS_PM2.5': self.get_pm2_5(),
            'SPS_PM10': self.get_pm10(),
            #'SPS_PM10s': self.get_pm10s()
            }
    
    def read_data(self):
        while not self.__sps.read_data_ready_flag():
            #print("New Measurement is not available!")
            if self.__sps.read_data_ready_flag() == self.__sps.DATA_READY_FLAG_ERROR:
                raise Exception("DATA-READY FLAG CRC ERROR!")

        if self.__sps.read_measured_values() == self.__sps.MEASURED_VALUES_ERROR:
            raise Exception("MEASURED VALUES CRC ERROR!")
        else:
            self.add_sampling_steps(1)
            self.add_pm1(self.__sps.dict_values['pm1p0'])
            self.add_pm2_5(self.__sps.dict_values['pm2p5'])
            self.add_pm10(self.__sps.dict_values['pm10p0'])
            self.add_pm10s(self.__sps.dict_values['pm10p0'])
