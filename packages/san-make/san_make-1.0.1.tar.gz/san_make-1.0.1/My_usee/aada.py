import os

from lxml import etree
def pos(name):
    s=os.popen('adb shell uiautomator dump').read()
    print(s)
    path=s.strip().split(' ',-1)[-1]
    os.system(f'adb pull {path} D:\\report')
    a=etree.parse("D:\\report\window_dump.xml")
    b=a.xpath(f'//*[@text="{name}"]')[0]
    z=b.get('bounds')
    z.replace('[','')
    return z


if __name__ == '__main__':
    z=pos(7)
    print(z)

