import busio
import digitalio
import board
import adafruit_mcp3xxx.mcp3008 as MCP
from adafruit_mcp3xxx.analog_in import AnalogIn

class GasSensor():

    def __init__(self):
        self.__CO = 0
        self.__NH3 = 0
        self.__NO2 = 0
        self.__sampling_steps_CO = 0
        self.__sampling_steps_NH3 = 0
        self.__sampling_steps_NO2 = 0
        
        # create the spi bus
        spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        # create the cs (chip select)
        cs = digitalio.DigitalInOut(board.D5)
        # create the mcp object
        mcp = MCP.MCP3008(spi, cs)

        # create an analog input channel on pin 0-2
        self.__channel_CO = AnalogIn(mcp, MCP.P0)
        self.__channel_NH3 = AnalogIn(mcp, MCP.P1)
        self.__channel_NO2 = AnalogIn(mcp, MCP.P2)
        
    def __del__(self):
        pass

    def read_data(self):
        if self.__channel_CO.value > 0:
            self.__CO += self.__channel_CO.value
            self.__sampling_steps_CO += 1
        if self.__channel_NH3.value > 0:
            self.__NH3 += self.__channel_NH3.value
            self.__sampling_steps_NH3 += 1
        if self.__channel_NO2.value > 0:
            self.__NO2 += self.__channel_NO2.value
            self.__sampling_steps_NO2 += 1

    def reset_data(self):
        self.__CO = 0
        self.__NH3 = 0
        self.__NO2 = 0
        self.__sampling_steps_CO = 0
        self.__sampling_steps_NH3 = 0
        self.__sampling_steps_NO2 = 0
        
    def set_nan_data(self):
        self.__CO = 'n/a'
        self.__NH3 = 'n/a'
        self.__NO2 = 'n/a'
        self.__sampling_steps_CO = 0
        self.__sampling_steps_NH3 = 0
        self.__sampling_steps_NO2 = 0
        
    def get_CO(self):
        return self.__CO
    
    def get_NH3(self):
        return self.__NH3
    
    def get_NO2(self):
        return self.__NO2
    
    def prepare_data(self):
        if self.__sampling_steps_CO > 0:
            self.__CO = (self.__CO / self.__sampling_steps_CO)
        if self.__sampling_steps_NH3 > 0:
            self.__NH3 = (self.__NH3 / self.__sampling_steps_NH3)
        if self.__sampling_steps_NO2 > 0:
            self.__NO2 = (self.__NO2 / self.__sampling_steps_NO2)
        
    def get_data(self):
        self.prepare_data()
        return {
            'CO': self.get_CO(),
            'NH3': self.get_NH3(),
            'NO2': self.get_NO2()
            }
