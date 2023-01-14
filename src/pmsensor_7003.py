from pms7003 import Pms7003Sensor, PmsSensorException
import pmsensor

class PMSensor7003(pmsensor.PMSensor):

    def __init__(self):
        super().__init__()
        self.__pms7003 = Pms7003Sensor('/dev/serial0')
        
    def __del__(self):
        self.__pms7003.close()

    def read_data(self):
        try:
            data = self.__pms7003.read()
            #print(data)
            self.add_sampling_steps(1)
            self.add_pm1(data['pm1_0'])
            self.add_pm2_5(data['pm2_5'])
            self.add_pm10(data['pm10'])
            self.add_pm10s(data['pm10'])
            # TODO: read function has option of returning values as dict or OrderedDict
            # https://github.com/tomek-l/pms7003
            # sensor.read(ordered=True)
            self.add_nc_0_3(data['n0_3'])
            self.add_nc_0_5(data['n0_5'])
            self.add_nc_1(data['n1_0'])
            self.add_nc_2_5(data['n2_5'])
            self.add_nc_5(data['n5_0'])
            self.add_nc_10(data['n10'])
        except PmsSensorException:
            print('Connection problem')      

    def get_data(self):
        self.prepare_data()
        return {
            '7003_PM1': self.get_pm1(),
            '7003_PM2.5': self.get_pm2_5(),
            '7003_PM10': self.get_pm10(),
            #'7003_PM10s': self.get_pm10s(),
            '7003_nc0.3': self.get_nc_0_3(),
            '7003_nc0.5': self.get_nc_0_5(),
            '7003_nc1': self.get_nc_1(),
            '7003_nc2.5': self.get_nc_2_5(),
            '7003_nc5': self.get_nc_5(),
            '7003_nc10': self.get_nc_10()
            }
    