import random
import time

from POM.common import Dr_get
from POM.custom_page import Page_customer
from POM.login_test import Logintest


class   Customertest:
    def __init__(self):
        self.dr = Page_customer()
    def test_new(self):
        phone=random.randint(111111111,999999999)
        time.sleep(3)
        self.dr.link_customer().click()
        time.sleep(2)
        self.dr.input_phone().send_keys(str(phone))
        time.sleep(2)
        self.dr.buton_new().click()
        time.sleep(2)
        self.dr.close()

if __name__ == '__main__':
    Logintest().login()
    c=Customertest().test_new()