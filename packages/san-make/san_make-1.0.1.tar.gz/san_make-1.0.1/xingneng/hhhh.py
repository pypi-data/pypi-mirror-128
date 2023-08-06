#coding=utf8
import csv,requests
import random,xlrd

from homework.con_db import Con_DB
cd = Con_DB('root','123456','woniuboss4.0')
def login():
    n=8
    for i in range(450):
        n=n+i
        employee_name0 = '讲师'
        work_id = 'WNCD02' + str(n)
        employee_name=employee_name0+str(n)
        department_id=7
        sex=random.choice(['男','女'])
        sql = f'''insert into employee(`region_id`,`department_id`,`work_id`,`employee_name`,`tel`,`email`,`qq`,`sex`,`position`,`emp_status`,`education`,`university`,`major`,`address`,`source`,`cardnum`,`emergency_contact`,`emergency_tel`,`emegency_relation`,`identity`,`birthday`,`birthday_type`,`entry_time`,`create_time`)
                        values("1","{department_id}","{work_id}","{employee_name}","13138912212","1231@11.com","12121213","{sex}","{employee_name0}","01","01","霍兹莫多","1313","13131恶的手段","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","1990-06-07","01","2020-07-17","2021-03-02");
                     '''
        cd.dml(sql)
    for i in range(270):
        n=n+i
        employee_name0 = '咨询师'
        work_id = 'WNCD01' + str(n)
        employee_name=employee_name0+str(n)
        department_id=2
        sex=random.choice(['男','女'])
        sql = f'''insert into employee(`region_id`,`department_id`,`work_id`,`employee_name`,`tel`,`email`,`qq`,`sex`,`position`,`emp_status`,`education`,`university`,`major`,`address`,`source`,`cardnum`,`emergency_contact`,`emergency_tel`,`emegency_relation`,`identity`,`birthday`,`birthday_type`,`entry_time`,`create_time`)
                        values("1","{department_id}","{work_id}","{employee_name}","13138912212","1231@11.com","12121213","{sex}","{employee_name0}","01","01","霍兹莫多","1313","13131恶的手段","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","1990-06-07","01","2020-07-17","2021-03-02");
                     '''
        cd.dml(sql)
    for i in range(180):
        n=n+i
        employee_name0 = '就业老师'
        work_id = 'WNCD00' + str(n)
        employee_name=employee_name0+str(n)
        department_id=3
        sex=random.choice(['男','女'])
        sql = f'''insert into employee(`region_id`,`department_id`,`work_id`,`employee_name`,`tel`,`email`,`qq`,`sex`,`position`,`emp_status`,`education`,`university`,`major`,`address`,`source`,`cardnum`,`emergency_contact`,`emergency_tel`,`emegency_relation`,`identity`,`birthday`,`birthday_type`,`entry_time`,`create_time`)
                        values("1","{department_id}","{work_id}","{employee_name}","13138912212","1231@11.com","12121213","{sex}","{employee_name0}","01","01","霍兹莫多","1313","13131恶的手段","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","达到阿德d","1990-06-07","01","2020-07-17","2021-03-02");
                     '''
        cd.dml(sql)
def quan():
    sql=f'''select * from employee where employee_id>8'''
    l=cd.query_all(sql)
    for i in l:
        name=i[3]
        pwd='DAF2ABB2A61A210C82E374AC2A5BFFD6'
        pwd2='DAF2ABB2A61A210C82E374AC2A5BFFD6'
        emil=i[6]
        phone=i[5]
        emp_id=i[0]
        sql=f'''insert into system_user(`name`,`pwd`,`pwd2`,`status`,`passwd_status`,`passwd2_status`,`icon`,`email`,`phone`,`employee_id`,`createdate`)
                values("{name}","{pwd}","{pwd2}","01","1","1","images/guest.jpg","{emil}","{phone}","{emp_id}","2021-03-03")
        '''
        cd.dml(sql)
def shouqun():
    sql = f'''select system_user.id,employee.position from system_user,employee where system_user.id=employee.employee_id and system_user.id>197'''
    l = cd.query_all(sql)
    print(l[0:3])
    role_ids = 0
    for i in l:
        user_id1=i[0]
        user_id=i[1]
        if user_id=='讲师':
            role_id=14
        elif user_id=='咨询师':
            role_id=13
            role_ids = 24
        elif user_id=='就业老师':
            role_id=15
        sql=f'''insert into system_user_role(`user_id`,`role_id`) values("{user_id1}","{role_id}");'''
        cd.dml(sql)
        if role_ids==24 and user_id=='咨询师':
            sql = f'''insert into system_user_role(`user_id`,`role_id`) values("{user_id1}","{role_ids}");'''
            cd.dml(sql)

def student():
    li=[]
    for i in range(10000):
        name='张三'+str(i)
        sex=random.choice(['男','女'])
        age=random.choice(['21','22','23','24','25','26'])
        zhuan='本科'
        xueyuan='霍格沃兹'
        zhuanye='计算机'
        jinyan=random.choice([1,2,3])
        phone='136'+str(random.randint(11111111,99999999))
        emal=str(i)+'@123.com'
        l=[name,sex,age,zhuan,xueyuan,zhuanye,jinyan,phone,emal,'8000','测试','自然流量']
        # l=f'[{name},{sex},{age},{zhuan},{xueyuan}，{zhuanye},{jinyan},{phone},{emal},8000,测试,自然流量]'
        li.append(l)
    with open('D:\qq download\woniuboss测试版4.0\测试版4.0\专属简历模板.csv','a+',encoding='utf-8',newline="\n") as f:
        w=csv.writer(f)

        w.writerows(li)

def fuquan(na):
    rq = requests.session()
    url = 'http://192.168.11.7:8080/woniuboss/login/userLogin'
    data = {'userName': 'WNCD000',
            'userPass': 'woniu123',
            'checkCode': '0000',
            'remember': 'Y'}
    res = rq.post(url=url, data=data)

    url1='http://192.168.11.7:8080/woniuboss/user/saveSetRole'
    data1 = {'userId': na,
             'roleId[]': '14'}
    res1 = rq.post(url=url1, data=data1)

def li():
    sql = '''select work_id from employee where position = '咨询师';'''
    l = cd.query_all(sql)
    li=[]
    lis=[]
    i=1
    for n in range(731587, 732572):
        i+=1
        li.append(n)
        if i%3==0:
            lis.append(li)
            li=[]
    return l,lis


def fen(n,j):
    rq = requests.session()
    url = 'http://192.168.11.7:8080/woniuboss/login/userLogin'
    data = {'userName': 'WNCD002',
            'userPass': 'Woniu1234',
            'checkCode': '0000',
            'remember': 'Y'}
    res = rq.post(url=url, data=data)
    url1='http://192.168.11.7:8080/woniuboss/allot/saveResourceToPool'
    data={'arr[]':n,'work_id':j}
    r=rq.post(url=url1, data=data)


def fem(i,j):
    sql=f'''update customer set work_id="{i}" where customer_id="{j}";'''
    cd.dml(sql)

if __name__ == '__main__':
    l,li=li()
    # print(l)
    x=732396
    for i in l[1:]:
        x+=1
        fem(i[0],x)







