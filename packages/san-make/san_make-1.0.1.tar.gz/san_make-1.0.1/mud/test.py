import itertools
import random

from mud.data import player, skills1, m1,m2,m3
from mud.services import init_monster, initmap, move, checkhit

# map=initmap()
# x=init_monster(map,)
# for i in range(50):
#     print(x[i])
# postion = random.sample(list(itertools.product(range(10), range(10))), 50)
# print(postion)
# mx={'x,y':(0,0)}
# ms=[]
# for i in range(50):
#     print(postion[i])
#     mx = {'x,y': (0, 0)}
#     mx['x,y']=postion[i]
#     ms.append(mx)
# # print(ms)
# from mud.view import display_battle
# player={'id':0,'name':'','hp':100,'mp':50,'damage':10,'defence':8,'x,y':(0,0),'skills':{}}
# postion = random.sample(list(itertools.product(range(10), range(10))), 50)
# while True:
#     positions=input('输入指令')
#     player=move(player,positions)
#     print(player['x,y'])
#     print(postion)
#     flag=checkhit(player)
#     if flag==True:
#         display_battle()
from mud.view import display_play, display_game
# player['skills']=skills1
# print(player['skills']['mp'])
# postion = random.sample(list(itertools.product(range(10), range(10))),50)
# m=[eval('m'+str(i+1))for i in range(3)]
# print(m)
# print(m)
# for i in range(50):
#     mx = random.choice(m)
#     mx['x,y']=(0,0)
#     mx['x,y']= postion[i]
#     mx['item'] = random.choice(item)
#     mx=mx
#     ms.append(mx)
with open('user.txt', 'r', encoding='utf-8') as f:
    users = f.readlines()
    for usre in users:
        usre.replace('\n','')
        print(usre)
    # for user in users:
    #     user = eval(str(user)-'\n')
    #     print(user)