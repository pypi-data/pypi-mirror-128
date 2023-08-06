import time

from app_ui.common.com import Com


class Test():
    def __init__(self):
        self.c=Com()
        self.dr=self.c.dr
    def test_login(self,phone,pwd,ex,res):
        # self.dr.find_element_by_id('com.modernsky.istv:id/txt_hot_city_item').click()
        time.sleep(1)
        self.dr.find_element_by_id('com.modernsky.istv:id/lin_view_me').click()
        time.sleep(1)
        self.dr.find_element_by_id('com.modernsky.istv:id/mChange').click()
        self.dr.find_element_by_id('com.modernsky.istv:id/mEditPhone').send_keys(phone)
        self.dr.find_element_by_id('com.modernsky.istv:id/mEditPwd').send_keys(pwd)
        self.dr.find_element_by_id('com.modernsky.istv:id/mLogin').click()
        time.sleep(1)
        if res=='success':
            self.dr.find_element_by_id('com.modernsky.istv:id/lin_view_me').click()
            time.sleep(1)
            t = self.dr.find_element_by_id('com.modernsky.istv:id/txt_bar_title').text
            if ex==t:
                print('ok')
            else:
                print('ko')
        else:
            t=self.dr.find_element_by_id('com.modernsky.istv:id/loginName').text
            if ex==t:
                print('ok')
            else:
                print('ko')


if __name__ == '__main__':

    li=[['15008477462','1136485op','个人中心','success'],['15008477462','1136485','密码登录','fail']]
    for i in li:
        z = Test()
        z.test_login(i[0],i[1],i[2],i[3])
