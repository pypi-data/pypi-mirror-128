import random

from ATM.action.custom_page import Page_customer


class   Customertest:
    def __init__(self):
        self.dr = Page_customer()
    def test_customer_add(self):
        phone=random.randint(111111111,999999999)
        self.dr.do_customer_add(phone)

