import time

from ATM.comon.common import Dr_get
from ATM.test.customer_test import Customertest
from ATM.test.login_test import Logintest


class Module:
    def prepare(self):
        n = Customertest()
        self.m = Logintest()
        self.n = n
    def main(self):
        self.m.main_login()
        # self.n.test_customer_add()
    def finish(self):
        self.n.dr.close()


if __name__ == '__main__':
    i=Module()
    i.prepare()
    i.main()
    i.finish()
