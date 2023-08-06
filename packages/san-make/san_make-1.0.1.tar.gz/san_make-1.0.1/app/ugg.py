import os
import time

class Svn:
    def __init__(self):
        self.svn_server_path='https://LAPTOP-00IBJ9DE:8443/svn/woniu/'
        self.svn_clietn_path='D:\\fghfg'
        self.tomcat_path="D:\\Programs\\apache-tomcat-8.0.42"
        # print(self.tomcat_path)
    def create(self):
        li=os.listdir(self.svn_clietn_path)
        if not li:
            os.system(f'svn  checkout {self.svn_server_path} {self.svn_clietn_path} --username=admin   --password=123456')
        os.system(f'svn  update  {self.svn_clietn_path}')

    def upda(self):
        os.system('taskkill /f /im java.exe')
        x=os.path.exists('{self.svn_clietn_path}\\woniusales.war')
        if x:
            os.system(f'del  /S  /Q {self.svn_clietn_path}\\woniusales.war')
        os.system(f'ant -f {self.svn_clietn_path}\\build.xml')
        li=os.listdir(f'{self.tomcat_path}\\webapps')
        print(li)
        if 'woniusales.war' in li:
            os.system(f'del  /S  /Q {self.tomcat_path}\\webapps\\woniusales.war')
        if 'woniusales' in li:
            os.system(f'rd   /S   /Q  {self.tomcat_path}\\webapps\\woniusales ')
        os.system(f'copy {self.svn_clietn_path}\\woniusales.war {self.tomcat_path}\\webapps\\woniusales.war ')
        time.sleep(2)
        os.system(f'{self.tomcat_path}\\bin\\startup.bat')
        while True:
            x=os.path.exists(f'{self.tomcat_path}\\webapps\\woniusales\\WEB-INF\\classes\\db.properties')
            if x :
                print(x)
                os.system('taskkill /f /im java.exe')
                break
            time.sleep(5)
        with open(f'{self.tomcat_path}\\webapps\\woniusales\\WEB-INF\\classes\\db.properties','w')as f:
            s='''db_url=jdbc:mysql://localhost:3306/woniusales?useUnicode=true&characterEncoding=utf8 
db_username=root
db_password=123456
db_driver=com.mysql.jdbc.Driver'''
            f.write(s)
        os.system(f'{self.tomcat_path}\\bin\\startup.bat ')

if __name__ == '__main__':
    s=Svn()
    s.create()
    s.upda()