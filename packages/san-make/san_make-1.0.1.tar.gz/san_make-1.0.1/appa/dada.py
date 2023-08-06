import copy
import re

import requests
import time
def get_bage():
    a=requests.get('https://app.mi.com/topList')
    b=a.text
    li=re.findall("href=\"/details\?id=(.*?)\"",b)
    li_1=list(set(li))
    # print(li_1)
    for i in li_1:
        c=requests.get(f'https://app.mi.com/details?id={i}')
        li1=re.findall("href=\"/download/(.*?)\"",c.text,re.S)
        # print(li1)
        if li1:
            d=requests.get(f'https://app.mi.com/download/{li1[0]}').content
            print(f'{i}正在下载')
            with open(f'D:\\测试\\app\\{i}.apk','ab') as f:
                f.write(d)
                print(f'{i}下载完成')

if __name__ == '__main__':
    z=1
    a=2
    c=z
    z=a
    a=c
    print(a,z)