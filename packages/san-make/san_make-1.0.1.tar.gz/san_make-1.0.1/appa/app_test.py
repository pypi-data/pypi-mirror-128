
import glob
import os
import time


class App_t:
    def __init__(self):
        self.page_list=glob.glob(r"D:/测试/app"+"/*.apk")
        self.datas=self.data()

    def get_photo(self,p):
        path = time.strftime(f'{p}-%H%M%S.png')
        os.system(f'adb shell screencap -p /sdcard/{path}')
        os.system(f'adb pull /sdcard/{path} D:\测试\\app\新建文件夹 (2)\\{path}')

    def data(self):
        data=[]
        for i in self.page_list:
            dic = {}
            r=os.popen(f'D:\sdk\\build-tools\\29.0.3\\aapt2 dump badging {i} |findstr package')
            r1=r.buffer.read().decode('unicode-escape')
            bag=r1.split(' ')[1].split('=')[1]
            r2 = os.popen(f'D:\sdk\\build-tools\\29.0.3\\aapt2 dump badging {i} |findstr launchable-activity')
            r3 = r2.buffer.read().decode('unicode-escape')
            act=r3.split(' ')[1].split('=')[1]
            dic['package']=bag.strip('\'')
            dic['Activity']=act.strip('\'')
            data.append(dic)
        return data


    def install(self):
        for i in self.page_list:
            try:
                r=os.popen(f'adb install -r {i}').read()
            except Exception as e:
                print(e)
            finally:
                pg=i[17:]
                # r=os.popen('adb shell pm list package -3').read()
                # print(r)
                if r=='':
                    print(f'{pg}安装过程成功')
                else:
                    print(f'{pg}安装过程失败')
                    self.get_photo(pg)
                time.sleep(2)

    def start(self):
        for i in self.datas:
            p=i['package']
            a=i['Activity']
            try:
                r=os.popen(f'adb shell am start -W -n {p}/{a}|findstr Status').read()
                r1 = os.popen(f'adb shell am start -W -n {p}/{a} |findstr WaitTime').read()
            except Exception as e:
                print(e)
            finally:
                t=r1.strip().split(':')[1]
                t1=r.strip().split(':')[1].strip()
                if t1=='ok':
                    print(f'{p}启动成功，启动时间为{t}')
                else:
                    print(f'{p}启动异常，启动时间为{t}')
                    self.get_photo(p)


    def text(self):
        for i in self.datas:
            p=i['package']
            a=i['Activity']
            log_path = time.strftime(f'{p}-%H%M%S.txt')
            os.system(f'adb shell monkey -p {p} -v -v --throttle 50 1000 > D:\\{log_path}')
            time.sleep(8)
            with open(f'D:\\{log_path}') as f:
                result = f.read()
            if 'anr' in result or 'ANR' in result:
                print(f'此次{p}应用执行monkey测试时出现了无响应，响应超时异常!')
                self.get_photo(p)
            else:
                print(f'此次{p}应用执行monkey测试时未出现无响应，响应超时异常.')
            if 'crash' in result or 'CRASH' in result:
                print(f'此次{p}应用执行monkey测试时出现了崩溃，闪退异常!')
                self.get_photo(p)
            else:
                print(f'此次{p}应用执行monkey测试时未出现崩溃，闪退异常.')
            if 'error' in result or 'EXCEPTION' in result:
                print(f'此次{p}应用执行monkey测试时出现了未知异常!')
                self.get_photo(p)
            if 'Monkey finished' in result:
                print(f'此次{p}应用在执行monkey测试时未出现任何异常.')

    def close(self):
        for i in self.datas:
            p=i['package']
            a=i['Activity']
            try:
                os.system(f'adb shell am force-stop {p}')
                time.sleep(1)
                r=os.popen(f'adb shell ps |findstr {p}').read()
            except Exception as e:
                print(e)
            # print(r)
            if not r:
                print(f'{p}关闭成功')
            else:
                print(f'{p}关闭异常')
                self.get_photo(p)

    def uninstall(self):
        for i in self.datas:
            p=i['package']
            # print(p)
            a=i['Activity']
            try:
                os.system(f'adb uninstall {p}')
                time.sleep(1)
                r=os.popen('adb shell pm list package -3').read()
            except Exception as e:
                print(e)
            if p not in r:
                print(f'{p}卸载成功')
            else:
                print(f'{p}卸载失败')
                self.get_photo(p)


    def main(self):
        s=input('输入测试类型')
        if s=='monkey':
            self.install()
            self.text()
            self.uninstall()
        else:
            self.install()
            self.start()
            self.close()
            self.uninstall()




if __name__ == '__main__':
    a=App_t().main()

