from gps3 import agps3

class Gps:
    def __init__(self):
        self.__lat = 0
        self.__lon = 0
        self.__alt = 0
        self.__time = 0
        self.__gps_socket = agps3.GPSDSocket()
        self.__data_stream = agps3.DataStream()

        self.__gps_socket.connect()
        self.__gps_socket.watch()

    def __del__(self):
        pass

    def compute_position(self):
        for new_data in self.__gps_socket:
            if new_data:
                self.__data_stream.unpack(new_data)
                self.__time = self.__data_stream.time
                self.__lat = self.__data_stream.lat
                self.__lon = self.__data_stream.lon
                self.__alt = self.__data_stream.alt
                return
    
    def get_lat(self):
        return self.__lat
    
    def get_lon(self):
        return self.__lon
    
    def get_alt(self):
        return self.__alt
    
    def get_time(self):
        return self.__time

    def get_data(self):
        return {
            'lat': self.__lat,
            'lon': self.__lon,
            'alt': self.__alt,
            'time': self.__time
            }
