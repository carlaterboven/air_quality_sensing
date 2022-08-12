# coding=utf-8
import RPi.GPIO as GPIO


class PMSensorSensirion:
    # RX and TX from Raspi side (switched on sensor side)
    GPIO_TX = 23    # sensor RX pin2
    GPIO_RX = 24    # sensor TX pin3

    def __init__(self):
        self.__pm1 = 0
        self.__pm2_5 = 0
        self.__pm10 = 0
        self.__pm10s = []
        self.__sampling_steps = 0

    def __del__(self):
        pass

    def get_pm1(self):
        return self.__pm1

    def get_pm2_5(self):
        return self.__pm2_5

    def get_pm10(self):
        return self.__pm10

    def get_pm10s(self):
        return self.__pm10s
