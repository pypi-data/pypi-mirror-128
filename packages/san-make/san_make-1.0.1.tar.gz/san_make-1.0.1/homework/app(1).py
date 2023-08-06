import random
import sys

from dteacher.con_db import Con_DB
from dteacher.utils import Utils
from flask import Flask,jsonify,request,render_template,make_response

app=Flask(__name__)
cd=Con_DB('root','123456','test')
utils=Utils()
import time
# class App:
#     def __init__(self,con_db,utils):
#         self.con_db = con_db      # 数据库操作类的对象
#         self.utils = utils
#         self.welcome()
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return jsonify({'code':'1004','message':'method erro'})
    else:
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        sql = f'select * from userinfo where account="{account}";'
        userinfo = cd.query_one(sql)   # 查询指定用户的信息
        if userinfo:  # 判断账号是否存在
                if passwd == userinfo[2]:  # 判断密码是否正确
                    res=make_response(jsonify({'code':'10001','message':'登录成功'}))
                    res.set_cookie('account',account,max_age=60)
                    return res
                else:
                    return jsonify({'code':'1002','message':'密码错误'})
        else:
            return jsonify({'code':'1003','message':'用户不存在'})
@app.route('/index',methods=['GET'])
def index():
    return render_template('login.html')
@app.route('/reg',methods=['GET','POST'])
def reg():
    if request.method=='GET':
        return jsonify({'code':'1004','message':'method erro'})
    else:
        account=request.form.get('account')
        passwd=request.form.get('passwd')
        realname=request.form.get('realname')
        phone=request.form.get('phone')
        sql = f'select * from userinfo where account="{account}";'
        userinfo = cd.query_one(sql)   # 查询指定用户的信息
        if not userinfo:
            sql = f'''insert into userinfo(`account`,`passwd`,`realname`,`phone`,`role`)
                     values("{account}","{passwd}","{realname}","{phone}","0");
                  '''
            cd.dml(sql)
            return jsonify({'code':'1001','message':'注册成功'})
        else:
            return jsonify({'code':'1002','message':'用户名已存在'})
# @app.route('/welcome',methods=['GET'])
# def welcome():
#     print('------ 欢迎使用蜗牛图书管理系统 -------')
#     print('------ 1 登录  2 注册  3 退出 -------')
#     s = input('请选择服务：')
#     if s == '1':
#         return
#     elif s == '2':
#         pass
#     else:
#         pass
# class Ordinary:
#     """非管理员"""
#     def __init__(self,userinfo,con_db,utils):
#         self.userinfo = userinfo      # 当前登录用户信息
#         self.con_db = con_db     # 数据库连接对象
#         self.utils=utils
#         # self.main()
#     def main(self):
#         while True:
#             print('------------ 请选择服务 ------------')
#             print('             1 借阅信息             ')
#             print('             2 图书查询             ')
#             print('             3 借阅图书             ')
#             print('             4 归还图书             ')
#             print('             5 退   出             ')
#             s = input('服务：')
#             if s == '1':
#                 self.query_borrow_info()
#             elif s == '2':
#                 self.query_book_info()
#             elif s == '3':
#                 self.borrow_book()
#             elif s == '4':
#                 self.return_book()
#             else:
#                 exit()
@app.route('/query_borrow_info',methods=['GET'])
def query_borrow_info():
    """查询借阅信息"""
    get_cookie=request.cookies.get('account')
    if get_cookie:
        account=get_cookie
        sql = f'select * from bookborinfo where account="{account}";'
        r = cd.query_all(sql)
        if bool(r):
            return jsonify({'code':'1001','message':'查询成功'})
        else:
            return jsonify({'code':'1002','message':'暂无借阅信息'})
    else:
        return jsonify({'code':'1003','message':'请登录系统'})
        # (f'{"序号":4}\t{"编号":4}\t{"书名":12}\t{"借阅日期":8}\t状态')
        # (f'{i+1:^4}\t{j[1]:4}\t{j[2]:12}\t{str(j[3]).split()[0]}\t{"已归还" if j[-1] else "未归还"}')
@app.route('/query_book_info/<string:a>',methods=['GET'])
def query_book_info(a):
    '''图书查询（支持编号、书名的模糊查询）'''
    get_cookie = request.cookies.get('account')
    if get_cookie:
        # a = request.args.get('bookid')
        sql = f'''select * from book where bookid="{a}" or name like "%{a}%";'''
        r = cd.query_all(sql)
        print(r)
        return jsonify({'code':'1001','message':'查询成功'})
    else:
        return jsonify({'code':'1002','message':'请登录系统'})
@app.route('/borrow_book',methods=['GET','POST'])
def borrow_book():
    '''借阅'''
    if request.method=='GET':
        return jsonify({'code':'1004','message':'method erro'})
    else:
        get_cookie = request.cookies.get('account')
        if get_cookie:
            account=get_cookie
            a=request.form.get('id')
            c=request.form.get('count')
            sql=f'select * from book where bookid ="{a}";'
            r=cd.query_one(sql)
            print(r)
            c=int(c)
            b=int(r[-1])
            if b>=c:
                m=b-c
                sql1=f'''update book set count= "{m}" where bookid="{a}";'''
                sql2=f'''insert into bookborinfo (`account`,`bookid`,`bro_date`)values("{account}","{a}","{utils.get_time()}");'''
                cd.dml(sql1,sql2)
                return jsonify({'code':'1001','message':'借阅成功'})
            else:
                return jsonify({'code':'1002','message':'图书数量不够'})
        else:
            return jsonify({'code':'1003','message':'请登录系统'})
@app.route('/return_book',methods=['GET','POST'])
def return_book():
    if request.method=='GET':
        return jsonify({'code':'1003','message':'method erro'})
    else:
        get_cookie = request.cookies.get('account')
        if get_cookie:
            account=get_cookie
            a=request.form.get('id')
            b=request.form.get('count')
            sql1 = f'''update book set count=(count+"{b}") where bookid="{a}";'''
            sql2 = f'''update bookborinfo set return_date="{utils.get_time()}" where bookid="{a}" and account="{account}";'''
            cd.dml(sql1,sql2)
            return jsonify({'code': '1001', 'message': '归还成功'})
        else:
            return jsonify({'code':'1002','message':'请登录系统'})
    #
    #
    # class Administrator(Ordinary):
    #     """管理员类，继承非管理员类"""
    #     def main(self):
    #         """重写父类方法"""
    #         while True:
    #             print('------ 请 选 择 服 务 ------')
    #             print('       1 借阅信息       ')
    #             print('       2 图书查询       ')
    #             print('       3 借阅图书       ')
    #             print('       4 归还图书       ')
    #             print('       5 添加图书       ')
    #             print('       6 删除图书       ')
    #             print('       7 退   出       ')
    #             s = input('服务：')
    #             if s == '1':
    #                 self.query_borrow_info()
    #             elif s == '2':
    #                 self.query_book_info()
    #             elif s == '3':
    #                 self.borrow_book()
    #             elif s == '4':
    #                 self.return_book()
    #             elif s == '5':
    #                 self.add_book()
    #             elif s == '6':
    #                 self.delete_book()
    #             else:
    #                 exit()
    #
@app.route('/add_book',methods=['GET','POST'])
def add_book():
    if request.method=='GET':
        return jsonify({'code':'1007','message':'method erro'})
    else:
        get_cookie = request.cookies.get('account')
        if get_cookie:
            account=get_cookie
            sql=f'select role from userinfo where account="{account}";'
            r=cd.query_one(sql)
            if r[0]=='1':
                a = request.form.get('id')
                b = request.form.get('name')
                c = request.form.get('author')
                d = request.form.get('count')
                sql=f'select * from book where bookid="{a}" and name="{b}" and author="{c}";'
                r=cd.query_one(sql)
                if bool(r):
                    sql=f'update book set count=(count+"{d}") where bookid ="{a}";'
                    cd.dml(sql)
                    return jsonify({'code':'1001','message':'添加成功'})
                else:
                    sql = f'select * from book where bookid="{a}";'
                    r = cd.query_one(sql)
                    if bool(r):
                        return jsonify({'code':'1003','message':'图书编号已存在'})
                    else:
                        sql = f'select * from book where name="{b}" and author="{c}";'
                        r = cd.query_one(sql)
                        if bool(r):
                            return jsonify({'code':'1004','message':'图书已存在'})
                        else:
                            sql = f'insert into book (`bookid`,`name`,`author`,`count`)values ("{a}","{b}","{c}","{d}");'
                            cd.dml(sql)
                            return jsonify({'code':'1002','message':'新增成功'})
            else:
                return jsonify({'code':'1005','message':'请登录管理员账号'})
        else:
            return jsonify({'code':'1006','message':'请登录系统'})
@app.route('/delete_book',methods=['GET','POST'])
def delete_book():
    if request.method=='GET':
        return jsonify({'code':'1005','message':'method erro'})
    else:
        get_cookie = request.cookies.get('account')
        if get_cookie:
            account = get_cookie
            sql = f'select role from userinfo where account="{account}";'
            r = cd.query_one(sql)
            if r[0] == '1':
                a=request.form.get('name')
                sql=f'select * from book where name="{a}";'
                r=cd.query_one(sql)
                if bool(r):
                    sql=f'''delete from book where name="{a}";'''
                    r=cd.dml(sql)
                    return jsonify({'code': '1001', 'message': '删除成功'})
                else:
                    return jsonify({'code': '1002', 'message': '图书不存在'})
            else:
                return jsonify({'code': '1003', 'message': '请登录管理员账号'})
        else:
            return jsonify({'code': '1004', 'message': '请登录系统'})
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4321,debug=True)


