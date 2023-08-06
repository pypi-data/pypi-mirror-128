import os
import re
import socket
import subprocess
import sys
import threading
import time

from app.asad import App


class Test:
    def __init__(self):
        self.l=[]
    def data(self):
        p=5000
        dp=6000
        de1=os.popen('adb devices').read()
        de2=re.findall('(.*?)	device',de1)
        de= de1.strip().split('\n')
        for i in de2:
            dic = {}
            devices=i.split('\t')[0]
            version = os.popen(f'adb -s {devices} shell getprop ro.build.version.release').read().strip()
            p=self.check_p(p)
            dp=self.check_p(dp)
            dic['udid']=devices
            dic['p']=p
            dic['dp']=dp
            dic['version']=version
            self.l.append(dic)
            p += 1
            dp += 1
        return self.l
    def check_p(self,p):
        while True:
            if self.de(p):
                p+=1
            else:
                return p
                break
    def de(self,p):
        con = socket.socket()
        try:
            con.connect(('127.0.0.1',p))
            return True
            con.shutdown(2)
        except:
            return False

    def run(self,p,bp,udid,version):
        # t=subprocess.run(f'start /b appium -a 127.0.0.1 -p {p} -bp {bp} -U {udid} --platform-version {version}',shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,encoding="utf-8")
        # print(t.stderr)
        # sys.path.append("/path/to/C:/Users/树先生/AppData/Roaming/npm/appium.cmd")
        # os.system(f'move C:/Users/树先生/AppData/Roaming/npm && start /b appium -a 127.0.0.1 -p {p} -bp {bp} -U {udid} --platform-version {version}')
        subprocess.Popen(f'start /b C:/Users/树先生/AppData/Roaming/npm/appium.cmd -a 127.0.0.1 -p {p} -bp {bp} -U {udid} --platform-version {version}',shell=True)
        time.sleep(4)
        App(udid,version,udid,p).app()
    def run_mokey(self,udid,package):
        u=udid.split(':')[1]
        log_path=time.strftime(f'{u}-%H%M%S.txt')
        print(log_path)
        os.system(f'adb -s {udid} shell monkey -p {package} -v -v --throttle 50 1000 > D:\\{log_path}')
        time.sleep(8)
        with open(f'D:\\{log_path}') as f:
            result=f.read()
        if 'anr' in result or 'ANR' in result:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时出现了无响应，响应超时异常!')
        else:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时未出现无响应，响应超时异常.')
        if 'crash' in result or 'CRASH' in result:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时出现了崩溃，闪退异常!')
        else:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时未出现崩溃，闪退异常.')
        if 'error' in result or 'EXCEPTION' in result:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时出现了未知异常!')
        if 'Monkey finished' in result:
            print(f'此次{package}应用在{udid}移动设备上执行monkey测试时未出现任何异常.')


if __name__ == '__main__':
    l=input('输入测试类型')
    if l=='appium':
        os.system('taskkill /f /im node.exe')
        t=Test()
        l=[]
        for i in t.data():
            th=threading.Thread(target=t.run,args=(int(i['p']),int(i['dp']),i['udid'],i['version']))
            th.start()
        th.join()
    else:
        t=Test()
        l = []
        for i in t.data():
            th=threading.Thread(target=t.run_mokey,args=(i['udid'],'com.miui.calculator'))
            l.append(th)
        for t in l:
            t.start()
        t.join()

