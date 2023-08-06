# coding=utf-8
'''
控制层
'''
import itertools
import random
import sys

from mud.services import page, regist, login, move, initmap, init_monster, init_player, checkhit, battle, postion, \
    get_item, save, load
from mud.view import display_main, display_regist, display_login, display_game, display_play, display_battle, \
    display_skill, display_get, display_gameover, display_adminlogin

pages=0
while True:
    # 显示主页
    if page=='main':
        display_main()
        pages=input('输入指令')
        if pages=='1':
            page='regist'
        if pages=='2':
            page='login'
        if pages=='3':
            sys.exit(0)
    elif page=='regist':
        display_regist()
        while True:
            name = input('输入用户名')
            passwd = input('输入密码')
            checkpasswd = input('确认密码')
            flag=regist(name, passwd, checkpasswd)
            if flag==True:
                page='login'
                break
    elif page=='login':
        display_login()
        name = input('输入用户名')
        passwd = input('输入密码')
        page=login(name, passwd)
    elif page=='adminlogin':
        display_adminlogin()
        name = input('输入用户名')
        passwd = input('输入密码')
        page = login(name, passwd)
    elif page=='game':
        display_game()
        pages = input('输入指令')
        map = (initmap())
        player = init_player(name)
        save('play.txt',player)
        if pages == '1':
            page = 'play'
            if page == 'play':
                monsters = init_monster()
                while True:
                    display_play()
                    position_=input('输入指令')
                    print(player['x,y'])
                    print(postion)
                    if position_=='5':
                        save('play.txt',player)
                    if position_=='6':
                        page='game'
                        break
                    player=move(player,position_)
                    # flag=checkhit(player)
                    # if flag==True:
                    #     display_battle()
                    # postion = random.sample(list(itertools.product(range(10), range(10))), 50)
                    # if player['x,y'] in postion:
                    flag=checkhit(player, postion)
                    if flag==True:
                        monster_name=monsters['name']
                        print(f'你遇到{monster_name}啦')
                        display_battle()
                        display_skill()
                        page=battle(player,monsters)
                        if page=='get_item':
                            display_get()
                            player=get_item(player,monsters)
                            print(player)
        elif pages == '2':
            for k,v in player.items():
                print(k,v)
        elif pages=='3':
            page = 'play'
            if page == 'play':
                monsters = init_monster()
                player=load('play.txt')
                while True:
                    display_play()
                    position_ = input('输入指令')
                    print(player['x,y'])
                    print(postion)
                    if position_ == '5':
                        save('play.txt',player)
                    if position_ == '6':
                        page = 'game'
                        break
                    player = move(player, position_)
                    # flag=checkhit(player)
                    # if flag==True:
                    #     display_battle()
                    # postion = random.sample(list(itertools.product(range(10), range(10))), 50)
                    # if player['x,y'] in postion:
                    flag = checkhit(player, postion)
                    if flag == True:
                        monster_name = monsters['name']
                        print(f'你遇到{monster_name}啦')
                        display_battle()
                        page = battle(player, monsters)
                        display_skill()
                        if page == 'get_item':
                            display_get()
                            player = get_item(player, monsters)
                            print(player)
        elif pages=='4':
            display_gameover()
            sys.exit(0)