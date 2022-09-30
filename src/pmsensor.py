class PMSensor:
        
    def __init__(self):
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s = []
        self.__sampling_steps = 0

    def __del__(self):
        # TODO turn off sensors
        pass
    
    def get_pm1(self):
        return self.__pm1

    def get_pm2_5(self):
        return self.__pm2_5

    def get_pm10(self):
        return self.__pm10

    def get_pm10s(self):
        return self.__pm10s
    
    def add_sampling_steps(self, value):
        self.__sampling_steps += value
    
    def add_pm1(self, value):
        self.__pm1 += value

    def add_pm2_5(self, value):
        self.__pm2_5 += value

    def add_pm10(self, value):
        self.__pm10 += value

    def add_pm10s(self, value):
        self.__pm10s.append(value)
    
    def reset_data(self):
        # TODO call in get methods instead of implicit reset like prepare data method
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s.clear()
        self.__sampling_steps = 0
        
    def set_nan_data(self):
        self.__pm1 = 'n/a'
        self.__pm2_5 = 'n/a'
        self.__pm10 = 'n/a'
        self.__pm10s.clear()
        self.__sampling_steps = 0

    def prepare_data(self):
        if self.__sampling_steps > 0:
            self.__pm1 = (self.__pm1 / self.__sampling_steps)
            self.__pm2_5 = (self.__pm2_5 / self.__sampling_steps)
            self.__pm10 = (self.__pm10 / self.__sampling_steps)
