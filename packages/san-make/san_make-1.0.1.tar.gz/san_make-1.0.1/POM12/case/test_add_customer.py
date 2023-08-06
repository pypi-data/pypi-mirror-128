from POM12.common.utils import *
import time
from POM12.case.test_login import Test_Login
class Test_Add_Customer:
    def __init__(self,brow):
        self.brow=brow
        self.driver = Test_Login(self.brow).login('admin','123456','0000')   # 登录
    def add_customer(self,phone,name,childdate):
        self.driver.find_element_by_link_text('会员管理').click()
        self.driver.find_element_by_id('customerphone').send_keys(phone)
        n = self.driver.find_element_by_id('customername')
        n.clear()
        n.send_keys(name)
        js = f'document.getElementById("childdate").value="{childdate}";'
        self.driver.execute_script(js)  # 执行js，给出生日期输入框设定值
        self.driver.find_element_by_xpath('//button[@onclick="addCustomer()"]').click() # 点击新增
    def test(self,info):
        data = get_data(info[3])   # 处理测试数据，返回一个列表
        result='success'
        self.add_customer(data[0],data[1],data[2])  # 登录操作
        # sql = 'delete from customer where customerid<>101;'
        # cd.dml(sql)  # 执行新增操作前清空会员数据，只保留id为101的一条数据
        self.driver.refresh()  # 刷新页面
        print(f'{self.brow}--{info[1]}--{info[0]}--',end='')
        sql = f'''select * from customer 
                  where customerphone="{data[0]}" and customername="{data[1]}" and childdate="{data[2]}";'''
        r = cd.query_one(sql)
        file = img_path + '/' + get_time() + info[0] + '.png'
        if info[-1] == 'success':
            try:
                assert bool(r) == True
                print('pass')
            except Exception:
                self.driver.save_screenshot(file)  # 如果用例执行失败，进行截图
                print('fail')
                result='fail'
            finally:
                sql=f'insert into report(`module`,`case`,`data`,`result`,`runtime`,`type`,`version`,`browser`) values("{info[1]}","{info[0]}","{data}","{result}",now(),"ui","v1.0","{self.brow}") '
                cd1.dml(sql)
        else:
            try:
                assert bool(r) == False
                print('pass')
            except Exception:
                self.driver.save_screenshot(file)  # 如果用例执行失败，进行截图
                print('fail')
                result='fail'
            finally:
                sql = f'insert into report(`module`,`case`,`data`,`result`,`runtime`,`type`,`version`,`browser`) values("{info[1]}","{info[0]}","{data}","{result}",now(),"ui","v1.0","{self.brow}") '
                cd1.dml(sql)

if __name__ == '__main__':
    file='D:\python test\\test_woniusales\data\\test_add_customer.csv'
    data=read_csv(file)
    t=Test_Add_customer()
    for i in data[1:]:
        t.test(i)
