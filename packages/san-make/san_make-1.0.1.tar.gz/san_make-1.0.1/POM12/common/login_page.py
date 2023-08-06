'''
页面类，继承页面基类（Base_Page）封装与业务流程相关的元素定位以及元素操作方法
'''
from selenium.webdriver.common.by import By
from selenium import webdriver
from POM12.common.base_page import Base_Page
class Login_Page(Base_Page):
    # 定位器，列出元素的定位方法
    username = (By.ID,'username')   # 定位用户输入框
    passwd = (By.ID,'password')
    code = (By.ID,'verifycode')
    login_bt = (By.XPATH,'/html/body/div[4]/div/form/div[6]/button')  # 登录按钮
    # 输入用户名
    def input_username(self,name):
        self.input(name,*self.username)
    # 输入密码
    def input_paswd(self,pwd):
        self.input(pwd,*self.passwd)
    # 输入验证码
    def inout_code(self,cd):
        self.input(cd, *self.code)
    # 点击登录按钮
    def click_login(self):
        self.click(*self.login_bt)

if __name__ == '__main__':
    drive=webdriver.Chrome()
    drive.get('http://localhost:8080/woniusales/')
    log=Login_Page(drive)
    log.input_username('admin')
    log.input_paswd('123456')
    log.inout_code('0000')
    log.click_login()







