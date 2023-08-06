# #coding=utf-8
# user=['admin''0000']
# flag=False
# #1.会员注册
# name = input('输入昵称')
# password = input('输入密码')
# checkword = input('确认密码')
# if 8<=len(name)<=20  and name.isalnum()==True and 6<=len(password)<=12 and checkword==password:
#     print('注册成功')
#     user.append(name)
#     user.append(password)
# else:
#     print('注册失败')
#     quit()
# #用户登录
# username=input('输入用户名')
# passwod=input('密码')
# i=1
# for n in range(5):
#     if username in user and passwod in user:
#         print('登录成功')
#         flag=True
#         break
#     else:
#         print('登录失败')
#         i=i+1
#         username = input('输入用户名')
#         passwod = input('密码')
#         if i==5:
#             print('账户已锁')
#             username = input('输入管理员用户名')
#             passwod = input('管理员密码')
#             if username=='admin' and passwod == '0000':
#                 print('登陆成功')
#                 i=1
#                 continue
#进入游戏
import random
import sys

map_width=10
map_high=10
map_master=[]
master1={'name':'公鸡','hp':100,'attack':10,'armor':5,'item':'剑'}
master2={'name':'猪','hp':100,'attack':10,'armor':5,'item':'盾'}
master3={'name':'野狗','hp':100,'attack':10,'armor':5,'item':'霜之哀伤'}
master4={'name':'稻草人','hp':100,'attack':10,'armor':5,'item':'反甲'}
masters=[master1,master2,master3,master4]
hp_man=0
hp_master=0
for a in range(50):
    x=random.randint(0,map_width-1)
    y=random.randint(0,map_high-1)
    map_master.append((x,y))
man_high=5
man_weigth=5
man={'hp':200,'mp':100,'attack':10,'armor':5}
kill=('普通攻击','kill1','kill2','kill3')
#普通攻击--》hp-10 kill1--》hp-20 kill2--》hp-30 kill3--》hp-30
item=()
print(man)
while True:
    #操作方向
    postion=input('输入')
    if postion=='w':
        man_high+=1
    if postion=='s':
        man_high-=1
    if postion=='a':
        man_weigth+=1
    if postion=='d':
        man_weigth-=1
    print(man_high,man_weigth)
    #战斗
    if (man_high,man_weigth) in map_master:
        print('进行战斗')
        for i in range(1):
            master = random.choice(masters)
            hp_man = man['hp'] + man['armor']
            hp_master = master['hp'] + master['armor']
            while hp_man>0:
                print('*'*5,'1.普通攻击','2.kill1','3.kill2','4.kill3','*'*5)
                skill=input('输入攻击方式')
                if skill=='1':
                    hp_master=hp_master-20
                    hp_man = hp_man-5
                elif skill=='2':
                    hp_master=hp_master-30
                    hp_man = hp_man-5
                elif skill=='3':
                    hp_master=hp_master-40
                    hp_man = hp_man- 5
                elif skill=='4':
                    hp_master=hp_master-50
                    hp_man = hp_man- 5
                print(hp_man,master)
                print(hp_master)
                if hp_master <= 0:
                    print('真不挫')
                    break
                if hp_man <= 0:
                    print('游戏结束')
                    sys.exit(0)









# while flag==True:
# print(x1map,y1map)
# for b in xmap:
#     for c in ymap:
#         if b == 10:
#             print('*' * b)














#进入游戏
