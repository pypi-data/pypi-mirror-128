#cording=utf-8
import xlrd
class Date:
    def __init__(self,excelname):
        self.filename=excelname
        self.book=xlrd.open_workbook(self.filename)
    def get_data(self,sheetname):
        sheet=self.book.sheet_by_name(sheetname)
        cols=sheet.ncols
        rows=sheet.nrows
        datacow=[]
        datacols=[]
        for i in range(rows) :
            datacow.append(sheet.row_values(i))
            print(sheet.row_values(i))
        # for i in range(cols):
        #     datacols.append(sheet.col_values(i))
        #     print(sheet.col_values(i))
        return datacow
    def get_dict(self,data):
        head=data[0]
        data=data[1:]
        items=[]
        for i in data:
            temp = {}
            temp[head[0]] = int(i[0])
            temp[head[1]] = i[1]
            temp[head[2]] = int(i[2])
            temp[head[3]] = int(i[3])
        items.append(temp)
        return items




if __name__=='__main__':
    datas=Date('data.xls')
    da=datas.get_data('sheet1')
    dat=datas.get_dict(da)
    print(dat)
    items1={'id':1,'name':'菜刀','type':1,'value':3}
    b=items1.items()
    print(b)