from config import ip, api_key

import requests
import time

import os

from huePyApi import Hue
from huePyApi.enums.Alert import Alert

from config import ip, api_key

# ToDo: code cleanup


def notify(title, text):
    print("Notification: title={}, text={}".format(title, text))
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


class HueStudyBreakTimer:
    def __init__(self, notification=False, room_id=0, temperature_notification=False, temperature_sensor=None,
                 temperature_limit=2100):
        self.hue = Hue.Hue(ip=ip, api_key=api_key)
        self.notification = notification
        self.temperature_notification = temperature_notification
        self.room = self.hue.get_group(room_id)
        self.room_all = self.hue.get_group(0)
        if temperature_sensor is not None:
            self.temperature = self.hue.get_sensor(temperature_sensor).get_temperature()
        self.temperature_limit = temperature_limit

    def blink(self, room, amount):
        for i in range(amount):
            room.set_alert(Alert.SELECT)
            time.sleep(0.8)

    def set_room_on(self):
        self.room.set_on(True)
        self.room.set_bri(250)
        self.room.set_ct(230)

    def read_temperature(self):
        if self.temperature_notification is True and self.temperature is not None:
            if self.temperature > self.temperature_limit:
                notify('Temperature', 'Temperature is {}°C. Turn down thermostat'.format(self.temperature / 100))
                time.sleep(3)

    def timer(self, planned_runtime_in_hours, learn_perioud_in_min, break_perioud_in_min):
        self.blink(self.room_all, 1)
        self.set_room_on()
        self.read_temperature()

        if self.notification is True:
            notify('StudyTimer started', 'you will be notified in ' + str(learn_perioud_in_min) + ' minutes')

        for i in range(planned_runtime_in_hours):
            time.sleep(learn_perioud_in_min * 60)
            if self.notification is True:
                notify('Make a break!', 'You deserve a little ' + str(break_perioud_in_min) + ' minute break :)')

            self.read_temperature()

            self.blink(self.room, amount=1)

            time.sleep(break_perioud_in_min * 60)

            if self.notification is True:
                notify('Break is over!',
                       'Continue your work :) Next break in ' + str(learn_perioud_in_min) + ' minutes')
            self.blink(self.room_all, amount=1)


if __name__ == '__main__':
    studyBreakTimer = HueStudyBreakTimer(temperature_sensor=86, notification=True, temperature_notification=True,
                                         room_id=1, temperature_limit=2100)
    studyBreakTimer.timer(planned_runtime_in_hours=10, learn_perioud_in_min=90, break_perioud_in_min=15)
