import time

import cv2
from PIL import ImageGrab
import os

from appium import webdriver

from appium_img.aada import pos, pos2


class Img_mai:
    def __init__(self):
        # self.app1 = {
        #     "platformName": "Android",
        #     "appPackage": "com.miui.calculator",
        #     "appActivity": "com.miui.calculator.cal.CalculatorActivity",
        #     "noReset":"True"
        #     }
        # self.app1["deviceName"]="appium"
        # self.app1["platformVersion"]="7.1.2"
        # self.app1["udid"]="127.0.0.1:62001"
        # self.d=webdriver.Remote('http://127.0.0.1:4723/wd/hub',self.app1)
        self.path=os.path.abspath('./imgs')
    def return_pos(self,name):
        # print(self.path+'/big.png')
        # self.d.save_screenshot('D:\python test\\appium_img\imgs\\big.jpg')
        os.system('adb shell screencap  -p /sdcard/big.jpg')
        os.system('adb pull /sdcard/big.jpg "D:\python test\\appium_img\imgs"')
        s=cv2.imread(self.path+f'\\{name}')
        b=cv2.imread('D:\python test\\appium_img\imgs\\big.jpg')
        result=cv2.matchTemplate(b,s,cv2.TM_CCOEFF_NORMED)
        # print(result)
        pos=cv2.minMaxLoc(result)
        # print(pos)
        x=pos[3][0] + int(s.shape[1]/2)
        y=pos[3][1] + int(s.shape[0]/2)
        if pos[1]>0.8:
            # print(x,y)
            return x,y
        else:
            return -1,-1
    def click(self,n):
        x,y=self.return_pos(n)
        self.d.tap([(x,y)],10)

    def start(self,p):
        os.system(f'adb shell am start -W -n {p}/com.miui.calculator.cal.CalculatorActivity')

    def click2(self,n):
        # x,y=self.return_pos(n)
        x,y=pos(n)
        os.system(f'adb shell input tap {x} {y}')
    def click3(self,n):
        x,y=pos2(n)
        os.system(f'adb shell input tap {x} {y}')

    def close(self,p):
        os.system(f'adb shell am force-stop {p}')
if __name__ == '__main__':
    # os.system('taskkill /f /im node.exe')
    # os.system('start /b C:/Users/树先生/AppData/Roaming/npm/appium.cmd')
    # time.sleep(5)
    t=Img_mai()
    t.start('com.miui.calculator')
    t.click2('8')
    time.sleep(1)
    t.click3('加')
    time.sleep(1)
    t.click2('3')
    time.sleep(1)
    t.click3('等于')
    time.sleep(1)
    # t.close('com.miui.calculator')
