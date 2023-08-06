import time,random
import xlsxwriter
class get_report:
    def __init__(self):
        #创建excel文件
        self.workbook = xlsxwriter.Workbook(f'D:\\python test\\test_book\\report\\report{random.randint(1,1000)}.xls')
        #在excel中创建工作表
        self.sheet_summary = self.workbook.add_worksheet('测试总况')

    #设置excel表格的列宽跟行高
    def set_sheet(self):
        #设置列的字母对应设置列宽
        self.sheet_summary.set_column("A:A",15)
        self.sheet_summary.set_column("B:E",20)
        #设置行高，第一行从0开始，这里从第二行开始开始设置
        self.sheet_summary.set_row(1,30)
        self.sheet_summary.set_row(2,30)
        self.sheet_summary.set_row(3,30)
        self.sheet_summary.set_row(4,30)
        self.sheet_summary.set_row(5,30)

    #设置表格的样式
    def set_format(self):
        #设置样式，这里设置两种样式style1 style2
        self.style1 = self.workbook.add_format({'bold':True,'font_size':18,'border':1})
        self.style2 = self.workbook.add_format({'bold':True,'font_size':14,'border':1})
        self.style1.set_align('vcenter')
        self.style2.set_align('vcenter')
        self.style1.set_align('center')
        self.style2.set_align('center')
        self.style1.set_bg_color("#70DB93")
        self.style1.set_color("#FFFFFF")

    #设置合并单元格以及插入表格内容
    def set_data(self,a,b,c,d):
        #合并单元格设置样式
        self.sheet_summary.merge_range('A1:E1','测试报告总概况',self.style1)
        self.sheet_summary.merge_range('A2:E2','测试概况',self.style2)
        self.sheet_summary.merge_range('A3:A6','项目图片',self.style2)
        #填写内容设置样式
        self.sheet_summary.write("B3","项目名称",self.style2)
        self.sheet_summary.write("B4","系统版本",self.style2)
        self.sheet_summary.write("B5","运行环境",self.style2)
        self.sheet_summary.write("B6","测试网络",self.style2)

        self.sheet_summary.write("C3","agileone",self.style2)
        self.sheet_summary.write("C4","V1.3",self.style2)
        self.sheet_summary.write("C5","windows 7",self.style2)
        self.sheet_summary.write("C6","外网",self.style2)

        self.sheet_summary.write("D3","用例总数",self.style2)
        self.sheet_summary.write("D4","通过总数",self.style2)
        self.sheet_summary.write("D5","失败总数",self.style2)
        self.sheet_summary.write("D6","测试日期",self.style2)

        self.sheet_summary.write("E3",a,self.style2)
        self.sheet_summary.write("E4",b,self.style2)
        self.sheet_summary.write("E5",c,self.style2)
        self.sheet_summary.write("E6",d,self.style2)

    #生成饼状图
    def set_pi(self):
        chart1 = self.workbook.add_chart({'type':'pie'})
        chart1.add_series({
            'name':'Agileone测试统计',
            'categories':'=测试总况!$D$4:$D$5',
            'values':'=测试总况!$E$4:$E$5',
        })
        chart1.set_title({'name':'Agileone测试统计'})
        # chart1.set_style(10)
        #指定插入报表的位置
        self.sheet_summary.insert_chart('A9',chart1)

    #生成柱状图
    def set_column(self):
        column_chart = self.workbook.add_chart({'type':'column'})
        column_chart.add_series({
            'name':'用例执行结果',
            'categories':'=测试总况!$D$4:$D$5',
            'values':'=测试总况!$E$4:$E$5',
        })
        column_chart.set_title({"name":"Agileone测试概况"})
        column_chart.set_y_axis({"name":"数量"})
        column_chart.set_x_axis({"name":"结果分类"})
        self.sheet_summary.insert_chart('A25',column_chart)

        self.workbook.close()
    def begin(self,a,b,c,d):
        self.set_sheet()
        self.set_format()
        self.set_data(a,b,c,d)
        self.set_pi()
        self.set_column()

if __name__=="__main__":
    d = get_report()
    print(time.strftime("%Y-%m-%d"))
    d.begin(5,3,2,time.strftime("%Y-%m-%d"))


