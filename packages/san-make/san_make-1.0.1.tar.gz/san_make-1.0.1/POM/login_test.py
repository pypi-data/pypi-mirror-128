import time

from POM.login_page import Page_login
class Logintest:
    def __init__(self):
        self.dr=Page_login()
    def login(self):
        self.dr.input_user().clear()
        self.dr.input_user().send_keys('admin')
        self.dr.input_pad().clear()
        self.dr.input_pad().send_keys('123456')
        self.dr.input_verfiy().clear()
        self.dr.input_verfiy().send_keys('0000')
        time.sleep(2)
        self.dr.buttun_login().click()

if __name__ == '__main__':
    m=Logintest().login()

