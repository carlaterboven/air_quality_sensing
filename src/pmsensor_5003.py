from pms5003 import PMS5003
import pmsensor

class PMSensor5003(pmsensor.PMSensor):

    def __init__(self):
        super().__init__()
        self.__pms5003 = PMS5003(
            device = '/dev/ttyAMA1',
            baudrate = 9600
        )

    def read_data(self):
        data = self.__pms5003.read()
        # print(data)
        self.add_sampling_steps(1)
        self.add_pm1(data.pm_ug_per_m3(1.0))
        self.add_pm2_5(data.pm_ug_per_m3(2.5))
        self.add_pm10(data.pm_ug_per_m3(10.0))
        self.add_pm10s(data.pm_ug_per_m3(10.0))
        self.add_nc_0_3(data.pm_per_1l_air(0.3))
        self.add_nc_0_5(data.pm_per_1l_air(0.5))
        self.add_nc_1(data.pm_per_1l_air(1.0))
        self.add_nc_2_5(data.pm_per_1l_air(2.5))
        self.add_nc_5(data.pm_per_1l_air(5.0))
        self.add_nc_10(data.pm_per_1l_air(10.0))

    def get_data(self):
        self.prepare_data()
        return {
            '5003_PM1': self.get_pm1(),
            '5003_PM2.5': self.get_pm2_5(),
            '5003_PM10': self.get_pm10(),
            #'5003_PM10s': self.get_pm10s(),
            '5003_nc0.3': self.get_nc_0_3(),
            '5003_nc0.5': self.get_nc_0_5(),
            '5003_nc1': self.get_nc_1(),
            '5003_nc2.5': self.get_nc_2_5(),
            '5003_nc5': self.get_nc_5(),
            '5003_nc10': self.get_nc_10()
            }
