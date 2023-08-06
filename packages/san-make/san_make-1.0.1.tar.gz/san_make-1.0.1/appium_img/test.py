import os
import random
import time


from pymouse import PyMouse
from pykeyboard import PyKeyboard
from selenium import webdriver

from My_usee.hghh import Img_mai


class Test_woniusales:
    def __init__(self):
        self.mymouse=PyMouse()
        self.mykeyboard=PyKeyboard()
        self.match=Img_mai()
    #点击
    def click(self,img_name):
        x,y=self.match.return_pos(img_name)
        self.mymouse.click(x,y)
    #清空输入值
    def clear_input(self):
        self.mykeyboard.press_keys([self.mykeyboard.control_key,"a"])
        time.sleep(0.5)
        self.mykeyboard.tap_key(self.mykeyboard.backspace_key)
    #下拉框操作
    def  select_test(self,num):
        for i in range(num):
            self.mykeyboard.tap_key(self.mykeyboard.down_key)
        self.mykeyboard.tap_key(self.mykeyboard.enter_key)
    #打开浏览器进入测试界面
    def input_keys(self,str):
        self.mykeyboard.type_string(str)
    def key(self,s):
        self.mykeyboard.press_key(s)
        self.mykeyboard.release_key(s)
    def unkey(self,li):
        self.mykeyboard.press_keys(li)
    def open_browser(self,url):
        u=webdriver.Chrome()
        u.get(url)
        u.maximize_window()
        # os.system(f'start /b \"C:\Program Files\Google\Chrome\Application\chrome.exe" {url}')
    def main_test(self):
        self.open_browser("http://localhost:8080/woniusales/")
        time.sleep(3)
        self.key(self.mykeyboard.shift_r_key)
        time.sleep(2)
        self.click("user.jpg")
        # self.key(self.mykeyboard.backspace_key)
        # self.input_keys("admin")
        # self.key(self.mykeyboard.backspace_key)
        # self.key(self.mykeyboard.backspace_key)
        self.unkey([self.mykeyboard.control_l_key,'v'])
        time.sleep(1)
        self.click("password.jpg")
        self.input_keys("123456")
        time.sleep(1)
        self.click("ver.jpg")
        self.input_keys("0000")
        time.sleep(1)
        self.click('login.jpg')
        time.sleep(2)
        self.click('customer.jpg')
        time.sleep(2)
        self.click("phone.jpg")
        num=random.randint(1111111111,9999999999)
        self.input_keys(str(num))
        time.sleep(2)
        self.click("add.jpg")
        time.sleep(2)
if __name__ == '__main__':
    t=Test_woniusales().main_test()

