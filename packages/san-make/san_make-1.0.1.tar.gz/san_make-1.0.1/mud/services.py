# coding=utf-8
'''
服务层
'''
import copy
import itertools
import random
import sys

from mud.data import m1, m2, m3, items1, items2, items3, items4, items5, items6, player, skills1, skills2, skills3, user

postion = random.sample(list(itertools.product(range(10), range(10))), 50)
page='main'

#注册
def regist(nickname,passwd,checkpass):
    if 8<=len(nickname)<=20  and nickname.isalnum()==True and 6<=len(passwd)<=12 and checkpass==passwd:
        print('注册成功')
        user[nickname]=passwd
        with open('user.txt','a',encoding='utf-8') as f:
            f.write(str(user)+'\n')
        flag=True
        return flag
    else:
        print('注册失败')
        flag=False
        return flag
#登录
def login(nickname,passwd):
    n = 1
    for i in range(5):
        with open('user.txt','r',encoding='utf-8') as f:
            users=f.readlines()
            for user in users:
                user.replace('\n','')
                user=eval(user)
                if user[nickname]==passwd:
                    print('登录成功')
                    page='game'
                    return page
                    break
                else:
                    print('登录失败')
                    n= n+1
                    nickname = input('输入用户名')
                    passwd = input('密码')
                    if n==5:
                        print('1.账户已锁,请联系管理员','2.退出')
                        x=input('输入指令')
                        if x=='1':
                            page='adminlogin'
                            return page
                            break
                        elif x=='2':
                            sys.exit(0)
            return False
#初始化地图
def initmap():
    width=10
    height=10
    return width,height
#初始化怪物
def init_monster():
    # ms = []
    m=[m1,m2,m3]
    item = [items1, items2, items3, items4, items5, items6]
    # postion = random.sample(list(itertools.product(range(10), range(10))),50)
    # print(postion)
    # for i in range(50):
    #     mx = random.choice(m)
    #     mx['x,y']=(0,0)
    #     mx['x,y']= postion[i]
    #     mx['item'] = random.choice(item)
    #     mx=mx
    #     ms.append(mx)
    mx = random.choice(m)
    mx['item'] = random.choice(item)
    return mx
#初始化角色
def init_player(nickname):
    player['name']=nickname
    skills=[skills1,skills2,skills3]
    player['skills']=skills
    return player
#角色移动
def move(player,direct=''):
    x=int(player['x,y'][0])
    y=int(player['x,y'][1])
    if direct=='w':
        player['x,y'] = (x, y + 1)
        if y>9:
            player['x,y'] = (x, 9)
            print('/t已经到达边界')
    elif direct=='s':
        player['x,y']= (x,y-1)
        if y<0:
            player['x,y'] = (x, 0)
            print('/t已经到达边界')
    elif direct=='a':
        player['x,y'] =(x-1,y)
        if x<0:
            player['x,y'] = (0, y)
            print('/t已经到达边界')
    elif direct=='d':
        player['x,y'] = (x+1,y)
        if x>9:
            player['x,y'] = (9, y)
            print('/t已经到达边界')
    return player
#检测碰撞
def checkhit(player,postion):
    if player['x,y'] in postion:
        return True
#发生战斗
def battle(player,master):
    for i in range(1):
        hp_man = player['hp'] + player['defence']
        hp_master = master['hp'] + master['defence']
        mp_man=player['mp']
        damage_man=player['damage']
        damage_master=master['damage']
        while hp_man > 0 :
            skill = input('输入攻击方式')
            if mp_man>=0:
                if skill == '1':
                    hp_master = hp_master - damage_man
                    hp_man = hp_man - damage_master
                    print(hp_man,hp_master,mp_man)
                elif skill == '2':
                    hp_master = hp_master - 30
                    hp_man = hp_man - damage_master
                    mp_man=mp_man-10
                    print(hp_man, hp_master,mp_man)
                elif skill == '3':
                    hp_master = hp_master - 50
                    hp_man = hp_man - damage_master
                    mp_man = mp_man - 20
                    print(hp_man, hp_master,mp_man)
                elif skill == '4':
                    hp_man = hp_man - damage_master+30
                    mp_man = mp_man - 30
                    print(hp_man, hp_master,mp_man)
            if hp_master <= 0:
                print('针不戳')
                player['hp']=hp_man
                player['mp']=mp_man
                page='get_item'
                return page
            if player['mp']<0:
                print('蓝量不足，不能使用技能')
                if skill == '1':
                    hp_master = hp_master - damage_man
                    hp_man = hp_man - damage_master
                    print(hp_man,hp_master,mp_man)
            if hp_man <= 0:
                print('游戏结束')
                sys.exit(0)
#装备拾取
def get_item(player,master):
    item=master['item']
    y=input(f'是否拾取装备{item} y/n')
    if y=='y':
        player['item']=item
        if item['type']==1:
            player['damage']=player['damage']+item['value']
        elif item['type']==2:
            player['defence'] = player['defence'] + item['value']
        elif item['type']==3:
            player['hp'] = player['hp'] + item['value']
    return player
#存盘
def save(filename,player):
    with open(filename,'a',encoding='utf-8') as f:
        f.write(str(player))
#读盘
def load(filename):
    with open(filename,'r',encoding='utf-8')as f:
        player=eval(f.read())
    return player


