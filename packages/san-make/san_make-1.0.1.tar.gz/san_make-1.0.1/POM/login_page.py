from POM.common import Dr_get
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