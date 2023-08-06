#coding=utf8
import requests,time,threading
import psutil
from xingneng.common import get_data, get_res

res_time=[]
res_get=[]

def get_run_time(func):
    def inner(self, *args, **kwargs):
        t1 = time.time()
        res = func(self, *args, **kwargs)
        t2 = time.time()
        print(f'响应时间：{int((t2 - t1) * 1000)}ms')
        res_time.append(int((t2 - t1) * 1000))
        return res
    return inner


class Search():
    def __init__(self):
        self.r=requests.session()
    @get_run_time
    def login(self):
        url='http://127.0.0.1:8080/woniusales/user/login'
        data={'username':'admin','password':'123456','verifycode':'0000'}
        res=self.r.post(url,data=data)
        print(f'发送登录请求,登录结果为{res.text}')
        x=get_res(res)
        print(f'获取登录请求大小为{x}Bety')
        res_get.append(x)

    @get_run_time
    def login_1(self):
        url = 'http://127.0.0.1:8080/woniusales/'
        res=self.r.get(url)
        x = get_res(res)
        print(f'获取登录请求大小为{x}Bety')
        res_get.append(x)
    @get_run_time
    def login_source(self):
        url1='http://127.0.0.1:8080/woniusales/library/css/bootstrap.css'
        url2='http://127.0.0.1:8080/woniusales/library/css/sitemain.css'
        url3='http://127.0.0.1:8080/woniusales/library/js/jquery-1.11.0.min.js'
        zurl=[url1,url2,url3]
        for i in zurl:
            res=self.r.get(url=i)
        print('获取登录资源')
    @get_run_time
    def hit_customer(self):
        url='http://127.0.0.1:8080/woniusales/customer'
        res=self.r.get(url)
        print('发送点击会员管理请求')
        x = get_res(res)
        print(f'获取登录请求大小为{x}Bety')
        res_get.append(x)
    @get_run_time
    def seacher(self):
        url='http://127.0.0.1:8080/woniusales/customer/search'
        data={'customerphone':'5454654654','page':'1'}
        res=self.r.post(url=url,data=data)
        print(f'发送查询会员请求,请求结果为{res.text}')
        x = get_res(res)
        print(f'获取登录请求大小为{x}Bety')
        res_get.append(x)

    def run_main(self):
        for i in range(1):
            self.login_1()
            time.sleep(1)
            self.login_source()
            time.sleep(1)
            self.login()
            time.sleep(2)
            self.hit_customer()
            time.sleep(1)
            self.seacher()

if __name__ == '__main__':
    a=Search()
    for i in range(1):
        th=threading.Thread(target=a.run_main)
        th.setDaemon(True)
        th.start()
    th.join()
    avg_t,max_t,min_t=get_data(res_time)
    avg_r,max_r,min_r=get_data(res_get)
    print(avg_t,max_t,min_t)
    print(avg_r,max_r,min_r)