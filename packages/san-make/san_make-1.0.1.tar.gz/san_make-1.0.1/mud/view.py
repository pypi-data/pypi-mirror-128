# coding=utf-8
'''
界面层
'''

#主页
def display_main():
    print('-' * 100)
    print('\t', '1.注册游戏'.ljust(20,'*'), '2.登录游戏'.center(30,'*'), '3.退出'.rjust(20,'*'))
    print('-' * 100)
#注册页面
def display_regist():
    print('-'*100)
    print('\t','注册账户'.center(80,'*'))
    print('\t', '输入用户名'.ljust(20,'*'),'输入密码'.center(30,'*'),'确认密码'.rjust(20,'*'))
    print('-'*100)
#登录页面
def display_login():
    print('-'*100)
    print('\t','登录账户'.center(80,'*'))
    print('-'*100)
#管理员登录界面
def display_adminlogin():
    print('-' * 100)
    print('\t', '管理员登录账户'.center(80, '*'))
    print('-' * 100)
#会员管理
def display_users():
    print('-' * 100)
    print('\t', '1.会员管理'.ljust(40, '*'),'2.playgame'.rjust(40,'*'))
    print('-' * 100)
#角色选择
def display_play():
    print('-'*100)
    print('\t','移动角色'.center(95,'*'))
    print('\t', '1.按w向上移动'.ljust(20,'*'),'2.按s向下移动'.center(20,'*'),'3.按a向左移动'.center(20,'*'),'4.按d向右移动'.rjust(20,'*'))
    print('\t', '5.存档'.ljust(45,'*'),'6.退出'.center(45, '*'))
    print('-'*100)
#游戏界面
def display_game():
    print('-'*100)
    print('\t','欢迎来到洛圣都'.center(90,'*'))
    print('\t', '1.开始游戏'.ljust(20,'*'),'2.显示角色'.center(20,'*'),'3.继续游戏'.center(20,'*'),'4.退出'.rjust(20,'*'))
    print('-'*100)
#遇敌界面
def display_checkhit():
    print('-'*100)
    print('\t','遇到怪物啦'.center(80,'*'))
    print('-'*100)
#战斗界面
def display_battle():
    print('-'*100)
    print('\t','batlle start'.center(80,'*'))
    print('-'*100)
#技能使用界面
def display_skill():
    print('-'*100)
    print('\t','1.普通攻击'.ljust(20,'*'),'2.农夫三拳'.center(20,'*'),'3.欧拉欧拉'.center(20,'*'),'4.砸哇唔多'.rjust(20,'*'))
    print('-'*100)
#拾取界面
def display_get():
    print('-'*100)
    print('\t','装备拾取'.center(80,'*'))
    print('-'*100)
#游戏结束界面
def display_gameover():
    print('-'*100)
    print('\t','game over'.center(80,'*'))
    print('-'*100)