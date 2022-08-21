from pms5003 import PMS5003

class PMSensor5003:

    def __init__(self):
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s = []
        self.__sampling_steps = 0
        self.__pms5003 = PMS5003(
            device = '/dev/ttyAMA0',
            baudrate = 9600
        )

    def __del__(self):
        pass

    def prepare_data(self):
        # TODO check for sampling steps > 0
        # TODO call in get methods instead of implicit reset and prepare data methods
        self.__pm1 = (self.__pm1 / self.__sampling_steps)
        self.__pm2_5 = (self.__pm2_5 / self.__sampling_steps)
        self.__pm10 = (self.__pm10 / self.__sampling_steps)

    def reset_data(self):
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s.clear()
        self.__sampling_steps = 0

    def read_data(self):
        data = self.__pms5003.read()
        # print(data)
        self.__sampling_steps += 1

        self.__pm1 += data.pm_ug_per_m3(1.0)
        self.__pm2_5 += data.pm_ug_per_m3(2.5)
        self.__pm10 += data.pm_ug_per_m3(10.0)

        self.__pm10s.append(data.pm_ug_per_m3(10.0))

    def get_pm1(self):
        return self.__pm1

    def get_pm2_5(self):
        return self.__pm2_5

    def get_pm10(self):
        return self.__pm10

    def get_pm10s(self):
        return self.__pm10s

    def get_data(self):
        return {
            'pm1': self.__pm1,
            'pm2.5': self.__pm2_5,
            'pm10': self.__pm10,
            'pm10_list': self.__pm10s
            }
