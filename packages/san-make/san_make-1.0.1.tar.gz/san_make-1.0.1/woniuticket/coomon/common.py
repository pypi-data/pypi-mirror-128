import os

import xlrd,requests,csv
base_url='http://192.168.255.180:14200'
rq=requests.session()

def get_data(n):
    li=[]
    li1=[]
    f=xlrd.open_workbook(r"D://qq download//接口测试用例.xls")
    print(f.sheets())
    sheet=f.sheet_by_index(n)
    rows=sheet.nrows
    for i in range(rows):
        x=sheet.row_values(i)
        li.append(x)
    for i in li[7:]:
        li1.append(i)
    t=li[0][1]
    url=base_url+li[1][1]
    method=li[2][1]
    dic={'t':t,'url':url,'method':method,'data':li1}
    return dic

def get_dic(n):
    l=n.split(',')
    dic={}
    for i in l:
        li=i.split('=')
        dic[li[0]]=li[1]
    return dic

def request_t(m,url,data=None):
    if m=='get':
        r=rq.get(url,params=data)
    if m =='post':
        r=rq.post(url=url,data=data)
    if m=='put':
        r=rq.put(url=url,data=data)
    if m=='delete':
        r=rq.request('DELETE',url,params=data)
    return r

def get_csv():
    f = xlrd.open_workbook(r"D://qq download//接口测试用例.xls")
    li=[]
    l=[]
    for i in range(15):
        sheet=f.sheet_by_index(i)
        row=sheet.nrows
        for n in range(row):
            r=sheet.row_values(n)
            li.append(r)
            if n==row-1:
                l.append(li)
                li=[]
    # print(l)
    for i in l:
        name=i[0][1]
        for n in i:
            with open(f'../csv/{name}.csv','a') as f:
                c=csv.writer(f)
                c.writerow(n)
                # print(i)








