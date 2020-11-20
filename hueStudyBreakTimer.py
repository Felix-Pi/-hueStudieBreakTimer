from config import ip, api_key

import requests
import time

import os


def notify(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))

class Hue:
    def __init__(self, ip, api_key, notification=False):
        self.ip = ip
        self.api_key = api_key
        self.api_url = 'http://' + self.ip + '/api/' + self.api_key
        self.notification = notification

    def request(self, room_id, query):
        url = self.api_url + '/groups/' + str(room_id) + '/action'
        return requests.put(url, query)

    def blink(self, room_id, amount):
        for i in range(amount):
            query = '{"alert": "select"}'
            hue.request(room_id, query)
            time.sleep(.8)

    def turn_on_room(self, room_id):
        query = '{' \
                '"on": true,' \
                ' "bri": 250,' \
                ' "hue": 39392,' \
                ' "sat": 13,' \
                ' "effect": "none",' \
                ' "xy": [0.3691,0.3719],' \
                ' "ct": 230,' \
                ' "colormode": "hs"' \
                '}'
        self.request(room_id, query)

    def timer(self, room_id, planned_runtime_in_hours, learn_perioud_in_min, break_perioud_in_min):
        self.turn_on_room(room_id)
        if self.notification is True:
            notify('StudyTimer started', 'you will be notified in ' + str(learn_perioud_in_min) + ' minutes')

        for i in range(planned_runtime_in_hours):
            time.sleep(learn_perioud_in_min * 60)
            if self.notification is True:
                notify('Make a break!', 'You deserve a little ' + str(break_perioud_in_min) + ' minute break :)')
            hue.blink(room_id, amount=3)

            time.sleep(break_perioud_in_min * 60)
            if self.notification is True:
                notify('Break is over!',
                       'Continue your work :) Next break in ' + str(learn_perioud_in_min) + ' minutes')
            hue.blink(room_id=0, amount=1)


if __name__ == '__main__':
    hue = Hue(ip=ip, api_key=api_key, notification=True)

    hue.timer(room_id=1, planned_runtime_in_hours=10, learn_perioud_in_min=60, break_perioud_in_min=5)
