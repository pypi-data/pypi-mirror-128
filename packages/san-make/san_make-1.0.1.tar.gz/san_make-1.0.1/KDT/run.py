#coding=utf8
from selenium import webdriver
import time
from KDT.case import Demo
from KDT.data import dataread

dr=webdriver.Chrome()
# dr.get('http://www.baidu.com')
dr.maximize_window()
l=dataread()
# print(l)
for i in l:
    li=i.strip().split(',')
    # print(li)
    d=Demo()
    args=li[1:]
    m=getattr(Demo,li[0])
    m(dr,*args)