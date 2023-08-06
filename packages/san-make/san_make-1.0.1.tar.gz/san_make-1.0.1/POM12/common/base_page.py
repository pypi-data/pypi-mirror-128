'''
POM，page object mode，实现页面元素与测试用例分离
封装页面基类，是所有页面类的基类，在类中封装页面操作常用方法
页面类，每一个页面封装一个类，在类中封装元素的定位以及元素的操作
'''
from selenium.webdriver.support.select import Select
import random
import time
class Base_Page:
    def __init__(self,driver):
        self.driver = driver
    def find_element(self,*args):
        '''定位一个元素'''
        return self.driver.find_element(*args)
    def find_elements(self,*args):
        '''定位一组元素'''
        return self.driver.find_elements(*args)
    def get_title(self):
        '''获取页面标题'''
        return self.driver.title
    def get_page(self):
        '''获取页面源码'''
        return self.driver.page_source
    def execute_js(self,js):
        '''执行js'''
        self.driver.execute_script(js)
    def accept_alert(self):
        '''在警告框中点击确定'''
        self.driver.switch_to.alert.accpet()
    def dismiss_alert(self):
        '''在警告框中点击取消'''
        self.driver.switch_to.alert.dismiss()
    def input_alert(self,msg):
        '''在警告框中点击取消'''
        self.driver.switch_to.alert.send_keys(msg)
    def frame_to(self,*args):
        '''切换到指定框架'''
        f = self.find_element(*args)   # 定位框架
        self.driver.switch_to.frame(f)  # 切换到框架
    def frame_outter(self):
        '''切换到外层框架'''
        self.driver.switch_to.default_content()
    def select_option(self,*args):
        '''随机选择下拉框选项'''
        s = self.find_element(*args)  # 定位下拉框
        option = len(Select(s).options)   # 获取选项数量
        Select(s).select_by_index(random.randint(0,option-1))  # 随机选择
    def input(self,msg,*args):
        '''输入内容'''
        ele = self.find_element(*args)  # 定位元素
        ele.clear()
        ele.send_keys(msg)
    def click(self,*args):
        '''点击还元素'''
        ele = self.find_element(*args)  # 定位元素
        ele.click()
    def get_img(self,file):
        '''截图'''
        self.driver.save_screenshot(file)
    def quit(self):
        '''关闭浏览器'''
        self.driver.quit()
    def close(self):
        '''关闭当前页面'''
        self.driver.close()
    def wait(self,t):
        '''隐式等待'''
        self.driver.implicitly_wait(t)
    def sleep(self,t):
        '''强制等待'''
        time.sleep(t)


