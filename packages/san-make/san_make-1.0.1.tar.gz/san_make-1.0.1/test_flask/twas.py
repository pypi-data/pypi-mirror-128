import datetime

s=((1, 'admin', 1, datetime.datetime(2021, 1, 20, 9, 51, 52), datetime.datetime(2021, 1, 20, 10, 1, 26)), (2, 'admin', 1, datetime.datetime(2021, 1, 20, 9, 52, 58), datetime.datetime(2021, 1, 20, 10, 1, 26)), (3, 'admin', 1, datetime.datetime(2021, 1, 20, 10, 0, 8), datetime.datetime(2021, 1, 20, 10, 1, 26)))
n={'id':'','account':'','bookid':'','time':'','rtime':''}
l=[]
for i in s:
    o=n.copy()
    o['id']=i[0]
    o['account']=i[1]
    o['bookid']=i[2]
    o['time']=i[3]
    o['rtime']=i[4]
    l.append(o)
print(l)


