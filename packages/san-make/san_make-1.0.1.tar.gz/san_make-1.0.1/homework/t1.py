#cording=utf-8
import threading,re

# def f(a,b):
#     print(a+b)
#
# f1=threading.Thread(target=f,args=(10,23))
# f2=threading.Thread(target=f,args=(20,34))
# f3=threading.Thread(target=f,args=(30,89))
# f1.start()
# f2.start()
# f3.start()
# print('hgj')


with open('untitled.html',encoding='utf-8') as a:
    s=a.read()
    s1=re.findall('a class="singleLink" (.+) title="" target="_blank">',s)
    s2=re.findall('<span class="text-links">(.+)</span>',s)
    a=dict(zip(s1[:-1],s2))
    print(a)

