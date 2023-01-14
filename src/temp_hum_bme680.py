import adafruit_bme680
import time
import board

class HumSensor():

    def __init__(self):
        self.__sampling_steps = 0
        self.__temperature = 0
        self.__rel_humidity = 0
        self.__pressure = 0

        i2c = board.I2C()   # uses SDA 23 and SCL 24 for i2c bus 3
        self.__bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        temperature_offset = 0 # TODO set this after colocation

    def __del__(self):
        pass

    def read_data(self):
        self.__temperature += self.__bme.temperature # +temperature_offset # in °C
        self.__rel_humidity += self.__bme.relative_humidity
        self.__pressure += self.__bme.pressure
        self.__sampling_steps += 1

    def reset_data(self):
        self.__temperature = 0
        self.__rel_humidity = 0
        self.__pressure = 0
        self.__sampling_steps = 0

    def set_nan_data(self):
        self.__temperature = 'n/a'
        self.__rel_humidity = 'n/a'
        self.__pressure = 'n/a'
        self.__sampling_steps = 0

    def get_temperature(self):
        return self.__temperature

    def get_rel_humidity(self):
        return self.__rel_humidity

    def get_pressure(self):
        return self.__pressure

    def prepare_data(self):
        if self.__sampling_steps > 0:
            self.__temperature = (self.__temperature / self.__sampling_steps)
            self.__rel_humidity = (self.__rel_humidity / self.__sampling_steps)
            self.__pressure = (self.__pressure / self.__sampling_steps)

    def get_data(self):
        self.prepare_data()
        return {
            'Temperature': self.get_temperature(),
            'Relative_Humidity': self.get_rel_humidity(),
            'Pressure': self.get_pressure()
            }
