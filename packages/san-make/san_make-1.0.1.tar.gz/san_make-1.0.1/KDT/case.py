#coding=utf8
import time
class Demo:
    @classmethod
    def goto(cls,dr,url):
        dr.get(url)
    @classmethod
    def input(cls, dr,obj,value):
        ob=obj.split('=',1)
        m=eval('dr.find_element_by_'+ob[0]+f'("{ob[1]}")')
        m.clear()
        m.send_keys(value)
        # if obj.startswith('id')==True:
        #     m=dr.find_element_by_id(obj[3:])
        #     m.clear()
        #     m.send_keys(value)
        # if obj.startswith('xpath')==True:
        #     m=dr.find_element_by_xpath(obj[6:])
        #     m.clear()
        #     m.send_keys(value)

    @classmethod
    def delay(cls,dr,li):
        time.sleep(int(li))

    @classmethod
    def singleclick(cls, dr, obj):
        # if obj.startswith('id') == True:
        #     m = dr.find_element_by_id(obj[3:])
        #     m.click()
        #
        # if obj.startswith('xpath') == True:
        #     m = dr.find_element_by_xpath(obj[6:])
        #     m.click()
        ob = obj.split('=', 1)
        m = eval('dr.find_element_by_' + ob[0] + f'("{ob[1]}")')
        m.click()



