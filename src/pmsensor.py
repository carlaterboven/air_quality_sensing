class PMSensor:
        
    def __init__(self):
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s = []
        self.__sampling_steps = 0
        # number concentrations in #/cm³ (sensirion sensor)
        # number concentratins per 0.1L air (PLANTOWER sensors)
        self.__nc_0_3 = 0
        self.__nc_0_5 = 0
        self.__nc_1 = 0
        self.__nc_2_5 = 0
        self.__nc_4 = 0
        self.__nc_5 = 0
        self.__nc_10 = 0

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
    
    def get_nc_0_3(self):
        return self.__nc_0_3
    
    def get_nc_0_5(self):
        return self.__nc_0_5
    
    def get_nc_1(self):
        return self.__nc_1
    
    def get_nc_2_5(self):
        return self.__nc_2_5
    
    def get_nc_4(self):
        return self.__nc_4
    
    def get_nc_5(self):
        return self.__nc_5
    
    def get_nc_10(self):
        return self.__nc_10
    
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
        
    def add_nc_0_3(self, value):
        self.__nc_0_3 += value
        
    def add_nc_0_5(self, value):
        self.__nc_0_5 += value
        
    def add_nc_1(self, value):
        self.__nc_1 += value
        
    def add_nc_2_5(self, value):
        self.__nc_2_5 += value
        
    def add_nc_4(self, value):
        self.__nc_4 += value
        
    def add_nc_5(self, value):
        self.__nc_5 += value
        
    def add_nc_10(self, value):
        self.__nc_10 += value
    
    def reset_data(self):
        # TODO call in get methods instead of implicit reset like prepare data method
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s.clear()
        self.__sampling_steps = 0
        self.__nc_0_3 = 0
        self.__nc_0_5 = 0
        self.__nc_1 = 0
        self.__nc_2_5 = 0
        self.__nc_4 = 0
        self.__nc_5 = 0
        self.__nc_10 = 0
        
    def set_nan_data(self):
        self.__pm1 = 'n/a'
        self.__pm2_5 = 'n/a'
        self.__pm10 = 'n/a'
        self.__pm10s.clear()
        self.__sampling_steps = 0
        self.__nc_0_3 = 'n/a'
        self.__nc_0_5 = 'n/a'
        self.__nc_1 = 'n/a'
        self.__nc_2_5 = 'n/a'
        self.__nc_4 = 'n/a'
        self.__nc_5 = 'n/a'
        self.__nc_10 = 'n/a'

    def prepare_data(self):
        if self.__sampling_steps > 0:
            self.__pm1 = (self.__pm1 / self.__sampling_steps)
            self.__pm2_5 = (self.__pm2_5 / self.__sampling_steps)
            self.__pm10 = (self.__pm10 / self.__sampling_steps)
            self.__nc_0_3 = (self.__nc_0_3 / self.__sampling_steps)
            self.__nc_0_5 = (self.__nc_0_5 / self.__sampling_steps)
            self.__nc_1 = (self.__nc_1 / self.__sampling_steps)
            self.__nc_2_5 = (self.__nc_2_5 / self.__sampling_steps)
            self.__nc_4 = (self.__nc_4 / self.__sampling_steps)
            self.__nc_5 = (self.__nc_5 / self.__sampling_steps)
            self.__nc_10 = (self.__nc_10 / self.__sampling_steps)
