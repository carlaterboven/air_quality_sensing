from pms7003 import Pms7003Sensor, PmsSensorException

if __name__ == '__main__':

    sensor = Pms7003Sensor('/dev/serial0')

    while True:
        try:
            print(sensor.read())
            # TODO: read function has option of returning values as dict or OrderedDict
            # https://github.com/tomek-l/pms7003
            # sensor.read(ordered=True)
        except PmsSensorException:
            print('Connection problem')

    sensor.close()
