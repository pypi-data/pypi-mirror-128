from selenium import webdriver
class Dr_get:
    dr=None
    @classmethod
    def get_dr(cls):
        if cls.dr==None:
            cls.dr=webdriver.Chrome()
            cls.dr.get('http://localhost:8080/woniusales')
            cls.dr.maximize_window()
        return cls.dr