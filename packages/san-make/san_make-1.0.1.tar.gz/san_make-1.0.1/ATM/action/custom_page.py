from ATM.comon.common import Dr_get


class Page_customer:
    def __init__(self):
        self.dr=Dr_get.get_dr()
    def link_customer(self):
        return self.dr.find_element_by_link_text('会员管理')
    def input_phone(self):
        return self.dr.find_element_by_id('customerphone')
    def buton_new(self):
        return self.dr.find_element_by_xpath('/html/body/div[4]/div[1]/form[2]/div[2]/button[1]')
    def close(self):
        return self.dr.close()
    def do_customer_add(self,phone):
        self.link_customer().click()
        self.input_phone().send_keys(phone)
        self.buton_new().click()