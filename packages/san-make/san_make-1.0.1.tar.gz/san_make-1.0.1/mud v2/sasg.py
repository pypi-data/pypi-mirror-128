#cording=utf-8
import xlrd,csv,pymysql
#
# book=xlrd.open_workbook('data.xls')
# sheet=book.sheet_names()
# print(sheet)
# sheet1=book.sheets()
# print(sheet1)
# b=book.sheet_by_name('sheet1')
# print(b)
# a=book.sheet_by_index(0)
# print(a)
# row=b.nrows
# print(row)
# for i in range(row):
#     n=a.row_types(i)
#     print(n)
# print(b.cell_value(1,1))
# col=b.ncols
# for i in range(row):
#     for j in range(col):
#         m=b.cell_value(i,j)
#         print(m)
# with open('as.csv',encoding='utf-8') as f:
#     r=csv.reader(f)
#     print(r)
#     for i in r:
#         print(i)

con=pymysql.connect(host='localhost',user='root',passwd='123456',port=3306,db='test',charset='utf8')
print(con)
cur=con.cursor()
sql='select * from userinfo;'
cur.execute(sql)
a=cur.fetchone()
print(a)
a=cur.fetchall()
print(a)
cur.close()
con.close()