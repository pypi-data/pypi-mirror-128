from selenium import webdriver
from POM12.common.utils import *
import time
class Test_Login:
    def __init__(self,brow):
        self.brow=brow
    def login(self,account,passwd,code):
        self.driver = open_browser(self.brow,base_url)
        self.driver.find_element_by_id('username').send_keys(account)  # 输入账号
        self.driver.find_element_by_id('password').send_keys(passwd)  # 输入密码
        self.driver.find_element_by_id('verifycode').send_keys(code)  # 输入验证码
        login_btn = self.driver.find_element_by_xpath('/html/body/div[4]/div/form/div[6]/button')
        login_btn.click()
        time.sleep(1)
        return self.driver
    def test(self,info):
        """
        测试函数
        :param info: 一条用例（列表）
        :return:
        """
        data = get_data(info[3])   # 处理测试数据，返回一个列表
        self.login(data[0],data[1],data[2])  # 登录操作
        print(f'{self.brow}--{info[1]}--{info[0]}--',end='')
        file = img_path + '/' + get_time() + info[0] + '.png'
        result='success'
        if info[-1] == 'success':
            try:
                assert '首页' not in self.driver.title
                assert '注销' in self.driver.page_source
                if '非管理员' not in info[0]:
                    assert '批次管理' in self.driver.page_source
                print('pass')
            except Exception:
                self.driver.save_screenshot(file)  # 如果用例执行失败，进行截图
                print('fail')
                result='fail'
            finally:
                sql=f'insert into report(`module`,`case`,`data`,`result`,`runtime`,`type`,`version`,`browser`) values("{info[1]}","{info[0]}","{data}","{result}",now(),"ui","v1.0","{self.brow}") '
                cd1.dml(sql)
                self.driver.quit()
        else:
            try:
                assert '首页' in self.driver.title
                print('pass')
            except Exception:
                self.driver.save_screenshot(file)
                print('fail')
                result = 'fail'
            finally:
                sql=f'insert into report(`module`,`case`,`data`,`result`,`runtime`,`type`,`version`,`browser`) values("{info[1]}","{info[0]}","{data}","{result}",now(),"ui","v1.0","{self.brow}") '
                cd1.dml(sql)
                self.driver.quit()
if __name__ == '__main__':
    file = 'D:\python test\\test_woniusales\data\\test_login.csv'
    data = read_csv(file)[1:]
    # print(data)
    tl = Test_Login()
    for i in data:
        tl.test(i)

