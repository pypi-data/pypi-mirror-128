import sys

from dteacher.con_db import Con_DB
from dteacher.utils import Utils
import time
class App:
    def __init__(self,con_db,utils):
        self.con_db = con_db      # 数据库操作类的对象
        self.utils = utils
        self.welcome()
    def login(self):
        # 接收外部输入的账号和密码
        print('-------------- 登录 ---------------')
        flag_1, flag_2 = True, True  # 控制内层和外层循环
        error = 0  # 计数器，保存密码连续错误次数
        while flag_1:
            account = input('账 号：')
            sql = f'select * from userinfo where account="{account}";'
            userinfo = self.con_db.query_one(sql)   # 查询指定用户的信息
            if userinfo:  # 判断账号是否存在
                while flag_2:
                    passwd = input('密 码：')
                    if passwd == userinfo[2]:  # 判断密码是否正确
                        print('登录成功')
                        if userinfo[-1] == '1':
                            a=Administrator(userinfo,self.con_db,utils)
                            a.main()
                        else:
                            Ordinary(userinfo,self.con_db,utils).main()
                    else:
                        error += 1
                        if error == 3:
                            print('密码已连续错误3次，程序结束')
                            flag_1, flag_2 = False, False
                        else:
                            print('密码错误，请重新输入')
                            flag_2 = self.utils.is_continue()
                            flag_1 = flag_2
            else:
                print('账号不存在')
                flag_1 = self.utils.is_continue()
    def reg(self):
        print('-------------- 注册 ---------------')
        flag_1, flag_2 = True, True  # 控制内层和外层循环
        while flag_1:
            account = input('账 号：')
            sql = f'select * from userinfo where account="{account}";'
            userinfo = self.con_db.query_one(sql)   # 查询指定用户的信息
            if not userinfo:
                passwd = input('密 码：')  # 长度6-10位，字母、数字、下划线组成
                realname = input('姓 名：')
                phone = input('手机号：')  # 纯数字、11位、1开头、（3，5，7，8）
                sql = f'''insert into userinfo(`account`,`passwd`,`realname`,`phone`,`role`)
                         values("{account}","{passwd}","{realname}","{phone}","0");
                      '''
                self.con_db.dml(sql)
                print('注册成功')
                flag_1 = False
            else:
                print('账号已存在，请重新输入')
                flag_1 = self.utils.is_continue()
    def welcome(self):
        print('------ 欢迎使用蜗牛图书管理系统 -------')
        print('------ 1 登录  2 注册  3 退出 -------')
        s = input('请选择服务：')
        if s == '1':
            self.login()
        elif s == '2':
            self.reg()
        else:
            self.con_db.close()
            sys.exit('再见！！！！！')
class Ordinary:
    """非管理员"""
    def __init__(self,userinfo,con_db,utils):
        self.userinfo = userinfo      # 当前登录用户信息
        self.con_db = con_db     # 数据库连接对象
        self.utils=utils
        # self.main()
    def main(self):
        while True:
            print('------------ 请选择服务 ------------')
            print('             1 借阅信息             ')
            print('             2 图书查询             ')
            print('             3 借阅图书             ')
            print('             4 归还图书             ')
            print('             5 退   出              ')
            s = input('服务：')
            if s == '1':
                self.query_borrow_info()
            elif s == '2':
                self.query_book_info()
            elif s == '3':
                self.borrow_book()
            elif s == '4':
                self.return_book()
            else:
                exit()

    def query_borrow_info(self):
        """查询借阅信息"""
        sql = f'''select bi.account,bi.bookid,b.name,bi.bro_date,bi.return_date from bookinfo bi,book b
                  where bi.account="{self.userinfo[1]}" and bi.bookid=b.bookid;'''
        r = self.con_db.query_all(sql)
        print(f'{"序号":4}\t{"编号":4}\t{"书名":12}\t{"借阅日期":8}\t状态')
        for i,j in enumerate(r):
            print(f'{i+1:^4}\t{j[1]:4}\t{j[2]:12}\t{str(j[3]).split()[0]}\t{"已归还" if j[-1] else "未归还"}')
    def query_book_info(self):
        '''图书查询（支持编号、书名的模糊查询）'''
        a=input('请输入查询信息')
        sql = f'''select * from book where bookid="{a}"or name like "%{a}%";'''
        r = self.con_db.query_all(sql)
        print(r)
        return r
    def borrow_book(self):
        '''借阅'''
        while True:
            a=input('请选择要借用的图书id')
            c=int(input('请选择借阅数量'))
            sql=f'select count from book where bookid ="{a}";'
            r=self.con_db.query_one(sql)
            b=int(r[0])
            if b>=c:
                m=b-c
                sql1=f'''update book set count= "{m}" where bookid="{a}";'''
                sql2=f'''insert into bookinfo (`account`,`bookid`,`bro_date`)values("{self.userinfo[1]}","{a}","{self.utils.get_time()}");'''
                self.con_db.dml(sql1,sql2)
                break
            else:
                d=input('图书数量不够，重选数量按1，不借按2')
                if d=='1':
                    continue
                else:
                    break

    def return_book(self):
        a=input('请输入要归还的图书id')
        b=input('请输入要归还的图书数量')
        sql = f'''update book set count=(count+"{b}") where bookid="{a}";'''
        #t = time.strftime('%Y-%m-%d %X')
        self.con_db.dml(sql)
        sql = f'''update bookinfo set return_date="{self.utils.get_time()}" where bookid="{a}";'''
        self.con_db.dml(sql)



class Administrator(Ordinary):
    """管理员类，继承非管理员类"""
    def main(self):
        """重写父类方法"""
        while True:
            print('------ 请 选 择 服 务 ------')
            print('         1 借阅信息         ')
            print('         2 图书查询         ')
            print('         3 借阅图书         ')
            print('         4 归还图书         ')
            print('         5 添加图书         ')
            print('         6 删除图书         ')
            print('         7 退    出         ')
            s = input('服务：')
            if s == '1':
                self.query_borrow_info()
            elif s == '2':
                self.query_book_info()
            elif s == '3':
                self.borrow_book()
            elif s == '4':
                self.return_book()
            elif s == '5':
                self.add_book()
            elif s == '6':
                self.delete_book()
            else:
                sys.exit(0)

    def add_book(self):
        flag=True
        while flag:
            a = input('请选择编号')
            b=input('请选择要添加的图书名')
            c = input('请选择作者名')
            d=input('请选择想要添加的图书数量')
            sql=f'select * from book where bookid="{a}" and name="{b}" and author="{c}";'
            r=self.con_db.query_one(sql)
            if bool(r):
                sql=f'update book set count=(count+"{int(d)}") where bookid ="{a}";'
                self.con_db.dml(sql)
                print('添加成功')
            else:
                sql=f'select * from book where bookid="{a}";'
                r = self.con_db.query_one(sql)
                if bool(r):
                    print('编号已存在')
                else:
                    sql = f'select * from book where name="{b}" and author="{c}";'
                    r = self.con_db.query_one(sql)
                    if bool(r):
                        print(f'{b}已存在')
                    else:
                        sql = f'insert into book (`bookid`,`name`,`author`,`count`)values ("{a}","{b}","{c}","{d}");'
                        self.con_db.dml(sql)
                        print('添加成功')
                        break
            flag = self.utils.is_continue()

    def delete_book(self):
        while True:
            a=input('请选择想要删除的图书')
            sql=f'select * from book where name="{a}";'
            r=self.con_db.query_one(sql)
            if bool(r):
                sql=f'delete from book where name = "{a}";'
                self.con_db.dml(sql)
                print('删除成功')
                break
            else:
                print('图书不存在')
if __name__ == '__main__':
    cd = Con_DB('root','123456','test')
    utils = Utils()
    app = App(cd,utils)



