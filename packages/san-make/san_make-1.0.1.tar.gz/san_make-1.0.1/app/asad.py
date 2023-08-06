import time

from appium import webdriver
class App():
    def __init__(self,deviceName,Version,udid,p):
        self.app1 = {
            "platformName": "Android",
            "appPackage": "com.miui.calculator",
            "appActivity": "com.miui.calculator.cal.CalculatorActivity",
            "noReset": "True"}
        self.app1["deviceName"]=deviceName
        self.app1["platformVersion"]=Version
        self.app1["udid"]=udid
        self.p=p
    def app(self):
        dr=webdriver.Remote(f'http://127.0.0.1:4723/wd/hub',self.app1)
        time.sleep(1)
        dr.find_element_by_id('com.miui.calculator:id/btn_9_s').click()
        dr.find_element_by_id('com.miui.calculator:id/btn_minus_s').click()
        dr.find_element_by_id('com.miui.calculator:id/btn_6_s').click()
        dr.find_element_by_id('com.miui.calculator:id/btn_equal_s').click()
        d=dr.find_elements_by_class_name('android.widget.TextView')[7]
        print(d.text)
        if int(d.text)==3:
            print('ok')
        else:
            print('fail')


if __name__ == '__main__':
    A=App('127.0.0.1:62025','7.1.2','127.0.0.1:62025')
    A.app()