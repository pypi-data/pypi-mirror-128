import os,time,csv,requests,hashlib,re
base_bath=os.path.dirname(os.path.dirname(__file__))
case_bath=os.path.join(base_bath,'case')
data_bath=os.path.join(base_bath,'data')
report_bath=os.path.join(base_bath,'report')
base_url='http://192.168.11.108:5000'
rq=requests.session()

def request(url,method,data,hearder=None):
    if method.lower()=='get':
        r=rq.get(url=url,params=data,headers=hearder)
    elif method.lower()=='post':
        r=rq.post(url=url,data=data,headers=hearder)
    return r

def get_time():
    return time.strftime('%Y-%m-%d %H-%M-%S')

def read_csv(file,charset='utf8'):
    with open(file,encoding=charset) as f:
        return list(csv.reader(f))

def get_data(s):
    dic={}
    tmp=s.split()
    for i in tmp:
        t=i.split('=')
        dic[t[0]]=t[1]
    return dic

def loginadmin():
    url='http://192.168.11.108:5000/login'
    data={'account':'admin','passwd':'admin123'}
    r=request(url,method='post',data=data)
    return r

def get_md5(s):
    return hashlib.md5(s.encode('utf8')).hexdigest()
def add_bug(module,title,steps):
    """
    在禅道中提交bug
    :param module:模块（序号）
    :param title:缺陷名称
    :param assignedTo:缺陷分配给谁
    :param steps:缺陷详细描述
    :param uid:禅道用户id
    :return:
    """
    url_login='http://47.92.203.151:8000/zentaopms/www/user-login.html'
    url_bug='http://47.92.203.151:8000/zentaopms/www/bug-create-2-0-moduleID=2.html'
    rq=requests.session()
    #对登录页面发起get请求，获取verifyRand
    r=rq.get(url=url_login)
    rand=re.findall("'verifyRand' value='(\d+)'  />",r.text)
    print(rand)
    data={'account':'admin','verifyRand':rand,
          'referer':'http://47.92.203.151:8000/zentaopms/www/my',
          'password':get_md5(get_md5('123456')+str(rand))}

    r=rq.post(url=url_login,data=data)
    print(r.text)
    r1 = rq.get(url=url_bug)
    print(r1.text)
    uid = re.findall("var kuid = '(\w+)';", r.text)
    print(uid)
    data={'product':(None,'2'),'module':(None,f'{module}'),'project':(None,'1'),
          'openedBuild[]':(None,'trunk'),'assignedTo':(None,'hanzhitai'),'type':(None,'codeerror'),
          'title': (None, f'{title}'), 'severity': (None, '3'), 'pri': (None, '2'),'steps': (None, f'{steps}'),
          'oldTaskID': (None, '0'),'uid': (None, '600bd980e6121')}
    r=rq.post(url=url_bug,files=data)
if __name__ == '__main__':
    r=add_bug('1','aas','asas')





