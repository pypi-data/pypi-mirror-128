#coding=utf-8
import requests,time,hashlib,base64
from Crypto.Cipher import AES
# url='http://127.0.0.1:4321/login'
# d={'account':'admin','passwd':'123456'}
# r=requests.post(url=url,data=d)
# c=dict(r.cookies)
# print(c)
# head={'Cookie':f'account={c["account"]}'}
# url='http://127.0.0.1:4321/query_borrow_info'
# r=requests.get(url,headers=head)
# print(r.json())
# url='http://47.92.203.151:8000/auth_get_event_list/'
# d={'eid':'1001'}
# user=('admin','sys123456')
# r=requests.get(url=url,params=d,auth=user)
# print(r.text)
# url='http://47.92.203.151:8000/token_login/'
# d={'username':'admin','password':'sys123456'}
# r=requests.post(url=url,data=d)
# token=r.json()['token']
# url='http://47.92.203.151:8000/api/token_get_event_list/'
# h={"Authorization":f"Token {token}"}
# r=requests.get(url=url,params={'eid':'1001'},headers=h)
# print(r.json())
# t=str(time.time()).split('.')[0]
# print(t)
# key='&Guest-Bugmaster'
# sign=hashlib.md5((t+key).encode('utf8')).hexdigest()
# print(sign)
# url='http://47.92.203.151:8000/sign_add_event/'
# d={'eid':'10001','time':t,'sign':sign}
# time.sleep(5)
# r=requests.post(url=url,data=d)
# print(r.json())
key='gsjhgasjhgajghgh'
iv=b"6736136712677667"
d='hdghgdhsgdhjgdgd'
aes=AES.new(key.encode('utf8'),AES.MODE_CBC,iv)
d=aes.encrypt(d.encode('utf8'))
print(d)
d=base64.urlsafe_b64encode(d)
print(d)
d1=base64.urlsafe_b64decode(d)
print(d)
aes1=AES.new(key.encode('utf8'),AES.MODE_CBC,iv)
d=aes1.decrypt(d1.decode('utf8'))
print(d)