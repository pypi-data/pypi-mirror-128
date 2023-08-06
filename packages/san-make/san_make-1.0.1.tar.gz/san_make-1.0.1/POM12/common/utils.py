import os,hashlib,re
import csv
import time
from .con_db import Con_DB
from selenium import webdriver

cd = Con_DB('root','123456','woniusales')  # 连接数据库
cd1=Con_DB('root','123456','test_repport')

# base_url = 'http://47.92.203.151:8080/woniusales/'
base_url = 'http://localhost:8080/woniusales/'

base_path = os.path.dirname(os.path.dirname(__file__))   # 获取项目路径
case_path = os.path.join(base_path,'case') # 测试脚本目录
data_path = os.path.join(base_path,'data') # 测试数据目录
report_path = os.path.join(base_path,'report')  # 测试报告目录
driver_path = os.path.join(base_path,'driver')  # 驱动目录
img_path = os.path.join(base_path,'img')  # 失败截图保存目录

def get_time():
    return time.strftime('%Y-%m-%d %H-%M-%S')

def read_csv(file,charset='UTF8'):
    """读取csv文件"""
    with open(file,encoding=charset) as f:
        return list(csv.reader(f))

def get_data(s):
    """处理测试数据，将'account=admin      \npassword=123456'变为列表['admin','123456']"""
    dic = []
    tmp = s.split()

    for i in tmp:  # i = 'password=123456'
        t = i.split('=')
        dic.append(t[1])
    return dic


def open_browser(browser,url):
    """
    根据传入的浏览器名称、url打开对应的浏览器
    :param browser: 浏览器名称
    :param url: 测试地址
    :return:
    """
    driver = None
    if browser.lower() in ('chrome','谷歌'):
        driver = webdriver.Chrome(executable_path='chromedriver')
    elif browser.lower() in ('firefox','火狐'):
        driver = webdriver.Firefox(executable_path='geckodriver')
    elif browser.lower() in ('edge'):
        driver = webdriver.Edge(executable_path='/msedgedriver')
    driver.maximize_window()
    driver.get(url)
    driver.implicitly_wait(30)  # 隐式等待
    return driver

if __name__ == '__main__':
    file = '/Users/my/PycharmProjects/class_78/test_woniusales/data/test_login.csv'
    data = read_csv(file)
    print(data)
    print(get_data(data[1][3]))
