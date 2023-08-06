import time

from ATM.action.login_page import Page_login
from ATM.comon.common import Dr_get


class Logintest:
    def __init__(self):
        self.dr=Page_login()
    def test_login(self,user,pwd,expect):
        self.dr.do_login(user,pwd)
        try:
            # self.dr.switch_get()
            time.sleep(1)
            self.dr.alert_get().click()
        finally:
            erro=0
            if expect=='失败':
                if '销售出库' not in self.dr.titie():
                    result='成功'
                else:
                    result='失败'
                    Dr_get.imagne()
                    erro=1
            else:
                if '销售出库'  in self.dr.titie():
                    result = '成功'
                else:
                    result = '失败'
                    Dr_get.imagne()
                    erro = 1
            return result,erro

    def main_login(self):
        l = Dr_get.data_get('D:\python test\ATM\data\login.csv')
        # print(l)
        for i in l[1:]:
            li=i.split(',')
            r, e = self.test_login(li[0], li[1], li[-1].strip())
            time.sleep(1)
            print(r, e)



