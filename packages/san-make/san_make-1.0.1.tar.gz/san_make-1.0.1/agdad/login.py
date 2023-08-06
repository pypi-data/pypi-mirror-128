import pymysql
def con_db():
    # 连接数据库
    con, cur=None,None
    try:
        con = pymysql.connect(user='root',
                          password='123456',
                          host='localhost',
                          port=3306,
                          db='test',
                          charset='utf8')
    except Exception as e:
        print(e)
    else:
        cur = con.cursor()  # 创建游标
    return con,cur
def is_continue():
    mark = input('继续输入请按1，结束请按任意键：')
    if mark == '1':
        return True
    return False
def login(cur):
    """
    登录
    :param cur: 游标
    :return:
    """
    # 接收外部输入的账号和密码
    print('----------- 登录 -----------')
    flag_1, flag_2 = True, True  # 控制内层和外层循环
    error = 0  # 计数器，保存密码连续错误次数
    while flag_1:
        account = input('账 号：')
        sql = f'select * from userinfo where account="{account}";'
        if cur.execute(sql) == 1:  # 判断账号是否存在
            info = cur.fetchone()  # 获取用户信息
            while flag_2:
                passwd = input('密 码：')
                if passwd == info[2]:  # 判断密码是否正确
                    print('登录成功')
                    flag_1, flag_2 = False, False
                else:
                    error += 1
                    if error == 3:
                        print('密码已连续错误3次，程序结束')
                        flag_1, flag_2 = False, False
                    else:
                        print('密码错误，请重新输入')
                        flag_2 = is_continue()
                        flag_1 = flag_2

        else:
            print('账号不存在')
            flag_1 = is_continue()


def regist(username,passwd,realname,phone):
    print('----------- 注册 -----------')
    flag_1, flag_2 = True, True  # 控制内层和外层循环
    error = 0  # 计数器，保存密码连续错误次数
    while True:
        con,cur=con_db()
        sql = f'select * from userinfo where account="{username}";'
        if cur.execute(sql) == 1:  # 判断账号是否存在
            print('账户名已存在')
        else:
            sql2=f'INSERT INTO `userinfo`(`account`, `passwd`, `realname`, `phone`, `role`) VALUES ("{username}","{passwd}","{realname}","{phone}","1"); '
            try:
                cur.execute(sql2)
            except Exception as a:
                print(a)
            else:
                con.commit()
                print('注册成功')
                break

if __name__ == '__main__':
    con,cur = con_db()   # 连接数据库，返回数据库连接对象与游标对象
    # login(cur)
    username=input('yhum')
    passwd=input('passwd')
    realname=input('zsxm')
    phone=input('phone')
    regist(username, passwd, realname, phone)
# 注册  