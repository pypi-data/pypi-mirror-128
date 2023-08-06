import pymysql
class Con_DB:
    def __init__(self,user,password,db,host='localhost',port=3306,charset='utf8'):
        self.user = user
        self.password = password
        self.db = db
        self.host = host
        self.port = port
        self.charset = charset
        self.con = None
        self.cur = None
        self.con_db()    #
    def con_db(self):
        try:
            self.con = pymysql.connect(user=self.user,
                                      password=self.password,
                                      host=self.host,
                                      port=self.port,
                                      db=self.db,
                                      charset=self.charset)
        except Exception as e:
            print(e)
        else:
            self.cur = self.con.cursor()
            # print('success')
    def query_all(self,sql):
        """查询返回多行数据"""
        try:
            self.cur.execute(sql)
            return self.cur.fetchall()
        except Exception as e:
            return str(e)
    def query_one(self,sql):
        """查询返回一行数据"""
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            return str(e)
    def dml(self,*sql):
        """DML操作"""
        try:
            for i in sql:
                self.cur.execute(i)
        except Exception as e:
            print(e)
            self.con.rollback()
            return str(e)
        else:
            self.con.commit()
            return True
    def close(self):
        self.cur.close()
        self.con.close()
if __name__ == '__main__':
    cd = Con_DB('root','root','woniusale',host='47.92.203.151')
    r = cd.query_one('select * from userinfo where account="user10011234567";')
    print(r)
    # r = cd.query_all('select * from userinfo;')
    # print(r)
    # s1 = 'update userinfo set role=1 where account="user4";'
    # s2 = 'update userinfo set role=0 where account="user500";'
    # cd.dml(s1,s2)

