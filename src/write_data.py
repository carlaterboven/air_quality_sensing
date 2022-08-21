import pandas as pd
import os

class DataLogger:
    def __init__(self, file):
        self.__file = file
        self.__logid = 0
        self.__has_header = False

    def __del__(self):
        pass
    
    def get_file(self):
        return self.__file
    
    def write_header(self):
        file = open(self.__file, 'w')
        file.write('LogID' + ',' + 'Time' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'Altitude' + ',' + 'PM2.5' + '\n')
        file.close()
        self.__has_header = True
        
    def write_data(self, gps_data, pmsensor_data):
        if self.__has_header is False:
            self.write_header()
        file = open(self.__file, 'a')
        file.write(str(self.__logid) + ',' + str(gps_data['time']) + ',' + str(gps_data['lat']) + ',' + str(gps_data['lon']) + ',' + str(gps_data['alt']) + ',' + str(pmsensor_data['pm2.5']) + '\n')
        file.close()
        self.__logid += 1
