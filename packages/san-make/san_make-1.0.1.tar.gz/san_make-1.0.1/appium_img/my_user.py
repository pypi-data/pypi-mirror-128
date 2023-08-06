import time,os
from pymouse import PyMouse
from pykeyboard import PyKeyboard

class Input_my:
    def __init__(self):
        self.m=PyMouse()
        self.k=PyKeyboard()
    def right_click(self,x,y):
        self.m.click(x,y,button=2)
    def light_click(self,x,y):
        self.m.click(x,y)
    def move(self,x,y):
        self.m.move(x,y)
    def input(self,str):
        self.k.type_string(str)
    def press(self,st):
        self.k.press_key(st)
        self.k.release_key(st)
    def nu_press(self,lis):
        self.k.processkey_key(lis)


if __name__ == '__main__':
    a=Input_my()
    time.sleep(5)
    a.move(762,355)
    a.light_click(762,355)
