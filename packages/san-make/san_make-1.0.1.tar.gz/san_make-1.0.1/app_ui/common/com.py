import os
import subprocess
import time

#coding=utf8
from appium import webdriver
class Com():
    def __init__(self):
        self.app1 = {
            "platformName": "Android",
            "appPackage": "com.modernsky.istv",
            "appActivity": "com.modernsky.istv.ui.activity.MainActivity",
            "noReset": "False"}
        self.app1["deviceName"]='127.0.0.1:62001'
        self.app1["platformVersion"]='7.1.2'
        self.app1["udid"] = '127.0.0.1:62001'
        os.system('taskkill /f /im node.exe')
        time.sleep(1)
        subprocess.Popen(f'start /b C:/Users/树先生/AppData/Roaming/npm/appium.cmd -a 127.0.0.1 -p 4723 -bp 6000 -U 127.0.0.1:62001 --platform-version 7.1.2',
            shell=True)
        time.sleep(4)
        self.dr = webdriver.Remote('http://127.0.0.1:4723/wd/hub', self.app1)
        self.start()
    def start(self):
        os.system(' adb shell am start -W -n  com.modernsky.istv/com.modernsky.istv.ui.activity.MainActivity')


if __name__ == '__main__':
    os.system('taskkill /f /im appium')
    c=Com()
