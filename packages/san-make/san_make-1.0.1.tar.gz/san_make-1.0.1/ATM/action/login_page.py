from ATM.comon.common import Dr_get


class Page_login:
    def __init__(self):
        self.dr=Dr_get.get_dr()
    def input_user(self):
        return self.dr.find_element_by_id('username')
    def input_pad(self):
        return self.dr.find_element_by_id('password')
    def input_verfiy(self):
        return self.dr.find_element_by_id('verifycode')
    def buttun_login(self):
        return self.dr.find_element_by_xpath('/html/body/div[4]/div/form/div[6]/button')
    def titie(self):
        return self.dr.title
    def close(self):
        return self.dr.close()
    def alert_get(self):
        return self.dr.find_element_by_xpath('/html/body/div[6]/div/div/div[3]/button')
    def do_login(self,user,pwd):
        self.input_user().clear()
        self.input_user().send_keys(user)
        self.input_pad().clear()
        self.input_pad().send_keys(pwd)
        self.input_verfiy().clear()
        self.input_verfiy().send_keys('0000')
        self.buttun_login().click()