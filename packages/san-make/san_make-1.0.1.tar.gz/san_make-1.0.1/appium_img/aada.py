import os
import re

from lxml import etree
def pos(name):
    s=os.popen('adb shell uiautomator dump').read()
    print(s)
    path=s.strip().split(' ',-1)[-1]
    os.system(f'adb pull {path} D:\\report')
    a=etree.parse("D:\\report\window_dump.xml")
    b=a.xpath(f'//*[@text="{name}"]')[0]
    z=b.get('bounds')
    m=re.findall('\d{1,}',z)
    x=int((int(m[0])+int(m[2]))/2)
    y=int((int(m[1])+int(m[3]))/2)
    return x,y

def pos2(n):
    s = os.popen('adb shell uiautomator dump').read()
    # print(s)
    path = s.strip().split(' ', -1)[-1]
    os.system(f'adb pull {path} D:\\report')
    a = etree.parse("D:\\report\window_dump.xml")
    b = a.xpath(f'//*[@content-desc="{n}"]')[0]
    z = b.get('bounds')
    m = re.findall('\d{1,}', z)
    x = int((int(m[0]) + int(m[2])) / 2)
    y = int((int(m[1]) + int(m[3])) / 2)
    return x, y

if __name__ == '__main__':
    z=pos(7)
    print(z)
    z='afaf'

