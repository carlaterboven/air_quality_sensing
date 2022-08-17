from gps3 import agps3
from time import sleep

gps_socket = agps3.GPSDSocket()
data_stream = agps3.DataStream()

gps_socket.connect()
gps_socket.watch()
file = open('../data/log.csv', 'a')
file.write('LogID' + ',' + 'Time' + ',' + 'Latitude' + ',' + 'Longitude' + ',' + 'Altitude' + '\n')
file.close()
log_id = 1

for new_data in gps_socket:
    if new_data:
        data_stream.unpack(new_data)
        print('Time: ', data_stream.time)
        print('Altitude: ', data_stream.alt)
        print('Latitude: ', data_stream.lat)
        print('Longitude: ', data_stream.lon)
        print(log_id)
        file = open('../data/log.csv', 'a')
        file.write(str(log_id) + ',' + str(data_stream.time) + ',' + str(data_stream.lat) + ',' + str(data_stream.lon) + ',' + str(data_stream.alt) + '\n')
        file.close()
        log_id += 1        


class Gps:
    # TODO maybe define PINs

    def __init__(self):
        self.__position = 0

    def __del__(self):
        pass

    def compute_position(self):
        pass

    def get_position(self):
        return self.__position
