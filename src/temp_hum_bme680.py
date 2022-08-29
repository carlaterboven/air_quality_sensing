import adafruit_bme680
import time
import board

class HumSensor():

    def __init__(self):
        self.__temperature = 0
        self.__rel_humidity = 0
        self.__pressure = 0
        # self.__gas = 0
        # self.__altitude = 0
        
        # Create sensor object, communicating over the board's default I2C bus
        i2c = board.I2C()   # uses board.SCL and board.SDA
        self.__bme = adafruit_bme680.Adafruit_BME680_I2C(i2c)
        # change this to match the location's pressure (hPa) at sea level
        self.__bme.sea_level_pressure = 1013.25
        # You will usually have to add an offset to account for the temperature of
        # the sensor. This is usually around 5 degrees but varies by use. Use a
        # separate temperature sensor to calibrate this one.
        #temperature_offset = -5
        temperature_offset = 0
        
    def __del__(self):
        pass

    def read_data(self):
        self.__temperature = self.__bme.temperature # +temperature_offset # in °C
        self.__rel_humidity = self.__bme.relative_humidity
        self.__pressure = self.__bme.pressure

    def reset_data(self):
        self.__temperature = 0
        self.__rel_humidity = 0
        self.__pressure = 0
        
    def get_temperature(self):
        return self.__temperature
    
    def get_rel_humidity(self):
        return self.__rel_humidity
    
    def get_pressure(self):
        return self.__pressure
        
    def get_data(self):
        #self.prepare_data()
        return {
            'Temperature': self.get_temperature(),
            'Relative_Humidity': self.get_rel_humidity(),
            'Pressure': self.get_pressure()
            }
    