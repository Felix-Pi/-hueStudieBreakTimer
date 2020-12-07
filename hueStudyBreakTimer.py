from config import ip, api_key

import requests
import time

import os

import huePyApi.Hue as hpi
from huePyApi.enums.Alert import Alert

from config import ip, api_key


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))


class HueStudyBreakTimer:
    def __init__(self, notification=False):
        self.hue = hpi.Hue(ip=ip, api_key=api_key)
        self.notification = notification

    def blink(self, room, amount):
        for i in range(amount):
            room.setAlert(Alert.SELECT)
            time.sleep(0.8)

    def timer(self, room_id, planned_runtime_in_hours, learn_perioud_in_min, break_perioud_in_min):
        room_all = self.hue.getGroup(0)

        room = self.hue.getGroup(room_id)
        room.setOn(True)
        room.setBri(250)
        room.setCt(230)

        if self.notification is True:
            notify('StudyTimer started', 'you will be notified in ' + str(learn_perioud_in_min) + ' minutes')

        for i in range(planned_runtime_in_hours):
            time.sleep(learn_perioud_in_min * 60)
            if self.notification is True:
                notify('Make a break!', 'You deserve a little ' + str(break_perioud_in_min) + ' minute break :)')
            self.blink(room, amount=1)

            time.sleep(break_perioud_in_min * 60)
            if self.notification is True:
                notify('Break is over!',
                       'Continue your work :) Next break in ' + str(learn_perioud_in_min) + ' minutes')
            self.blink(room_all, amount=1)


if __name__ == '__main__':
    studyBreakTimer = HueStudyBreakTimer(notification=True)
    studyBreakTimer.timer(room_id=1, planned_runtime_in_hours=10, learn_perioud_in_min=90, break_perioud_in_min=15)
