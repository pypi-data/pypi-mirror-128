import time

import pymysql
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
    @classmethod
    def data_get(cls,file):
        with open(file,encoding='utf8') as f:
            data=f.readlines()
        return data

    @classmethod
    def imagne(cls):
        phonename='..\imagne'+time.strftime('-%H%M%S.png')
        cls.dr.save_screenshot(phonename)
        return phonename

    @classmethod
    def con_db_dql(cls,version,module,types,title,result,error,image):
        con=pymysql.connect(user='root',password='123456',host='localhost',port='8080',db='cbtreport',charset='utf8')
        cur=con.cursor()
        sql=f'insert into cbtreport(testversion,testmodule,testtype,casetitle,testresult,testerror,testimage,testtime) values("{version}","{module}","{types}","{title}","{result}","{error}","{image}",now())'
        cur.execute(sql)
        cur.fetchall()
        cur.close()
        con.close()

    @classmethod
    def con_db_dml(cls,sql):
        con = pymysql.connect(user='root', password='123456', host='localhost', port='8080', db='cbtreport',
                              charset='utf8')
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        cur.close()
        con.close()


    @classmethod
    def report_get(cls,old,new):
        file='..\\report'+'report_woniu'+time.strftime('-%H%M%S.html')
        with open('D:\python test\ATM\\report\\report_sample.html',encoding='utf8',mode='a+') as f:
            m=f.read()
            m.replace(old,new)
        with open(file,encoding='utf8',mode='a+') as f:
            f.write(m)


