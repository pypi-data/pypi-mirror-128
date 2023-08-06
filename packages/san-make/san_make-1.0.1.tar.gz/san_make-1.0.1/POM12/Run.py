from POM12.common.utils import *
import os,sys,threading
def run(brow):
    files = os.listdir(data_path)  # 获取data_path目录下所有测试用例文件的名称
    for i in files:
        n = str(i.split('.')[0])
        data = read_csv(os.path.join(data_path, i))[1:]
        x = 'test_woniusales.case.' + n
        __import__(x)
        m = sys.modules[x]
        r = getattr(m, n.title())
        obj = r(brow)
        for i in data:
            obj.test(i)
            time.sleep(2)
        obj.drive.quit()
def report(version,test_type):
    case_total, case_pass, case_fail, case_skip, rate=0, 0, 0, 0, 0
    case_date = 0  # 测试日期
    # 查询用例总数
    sql = f'select count(*) from report where type="{test_type}" and version="{version}" ;'
    case_total =cd1.query_one(sql)[0]
    # 查询通过用例总数
    sql=f'select count(*) from report where type="{test_type}" and version="{version}" and result = "success";'
    case_pass = cd1.query_one(sql)[0]
    # 查询失败用例总数
    sql=f'select count(*) from report where type="{test_type}" and version="{version}" and result = "fail";'
    case_fail = cd1.query_one(sql)[0]
    # 查询跳过用例总数
    case_skip= int(case_total)-int(case_pass)-int(case_fail)
    # 查询测试日期
    sql = f'select distinct runtime from report where type="{test_type}" and version="{version}";'
    case_date = str(cd1.query_one(sql)[0]).split()[0]
    # 通过率
    rate = f'{int(case_pass)*100/int(case_total):.2f}%'
    print(case_pass,case_fail,case_skip)
    with open(report_path + '/result_demo.html',encoding='utf8') as f:
        s = f.read()
        s = s.replace('&version', version)
        s = s.replace('&date', case_date)
        s = s.replace('&tester','zz')
        s = s.replace('&total',str(case_total))
        s = s.replace('&pass',str(case_pass))
        s = s.replace('&fail',str(case_fail))
        s = s.replace('&skip',str(case_skip))
        s = s.replace('&rate',str(rate))
    module_total, module_pass, module_fail, module_skip = 0, 0, 0, 0
    sql = f'''select module,count(*) from report 
                      where type="{test_type}" and version="{version}"
                      group by module;'''
    module_total = cd1.query_all(sql)
    # 查询每个模块通过的用例数
    sql = f'''select module,count(*) from report 
                              where type="{test_type}" and version="{version}" and result="success"
                              group by module;'''
    module_pass = cd1.query_all(sql)
    # 查询每个模块失败的用例数
    sql = f'''select module,count(*) from report 
                              where type="{test_type}" and version="{version}" and result="fail"
                              group by module;'''
    module_fail = cd1.query_all(sql)
    # 查询每个模块跳过的用例数
    sql = f'''select module,count(*) from report 
                              where type="{test_type}" and version="{version}" and result="skip"
                              group by module;'''
    module_skip = cd1.query_all(sql)
    detail = ''  # 保存每个模块用例信息
    print(module_total,module_pass,module_fail,module_skip)
    for i, j in enumerate(module_total):
        m, t, p, f, sk = 0, 0, 0, 0, 0  # 模块、用例数、通过数、失败数、跳过数
        print(i,j)
        m = j[0]  # 模块
        t = j[1]  # 用例数
        if not module_pass:
            pass
        elif j[0] in module_pass[i]:
            p = module_pass[i][1]
        if not module_fail:
            pass
        else:
            for n in module_fail:
                if m==n[0]:
                    f = module_fail[i][1]
        if not module_skip:
            pass
        elif j[0] in module_skip[i]:
            sk = module_skip[i][1]
        detail += f'''<tr>
    					<td class="bottom" width="180">{i+1}</td>
    					<td class="bottom">{m}</td>
    					<td class="bottom">{t}</td>
    					<td class="bottom">{p}</td>
    					<td class="bottom">
                            <a href="{m}12.html" style="color:red;">{f}</a>
                        </td>
    					<td class="bottom">{sk}</td>
    				    </tr>'''

    # 以读模式打开html格式的失败的测试用例模板
        with open(f'{report_path}/module_demo.html',encoding='utf8') as f1:
            page = f1.read()
            # 将每个模块的模块名对html模板中的&module进行替换
            page = page.replace('&module', m)
            # 将每个模块的用例数对html模板中的&total进行替换
            page = page.replace('&total',str(t))
            # 将每个模块的用例通过数对html模板中的&pass进行替换
            page = page.replace('&pass',str(p))
            # 将每个模块的用例失败数对html模板中的&fail进行替换
            page = page.replace('&fail', str(f))
            # 将每个模块的用例跳过数对html模板中的&skip进行替换
            page = page.replace('&skip', str(sk))
            # 查询每个模块失败的用例(返回元组形式)
            sql = f'select * from report where type="{test_type}" and version="{version}" and module="{m}" and result="fail";'
            cases = cd1.query_all(sql)
            print(cases)
            # 声明空字符串用以保存每个模块失败的用例信息
            case_detail = ''
            # 通过枚举的方式遍历每个模块失败用例信息(i用于保存元素的索引,j用于保存获取到的元素值)
            for i, j in enumerate(cases):
                # 将每个模块的失败用例信息整理成html标记语言
                case_detail += f'''
                            <tr>
                                <td class="bottom" >{i+1}</td>
                                <td class="case" >{j[2]}</td>
                                <td class="bottom">{j[1]}</td>
                                <td class="case" >{j[3]}</td>
                                <td class="bottom">{j[4]}</td>
                            </tr>
                            '''
                # 替换html失败的测试用例模板的table模块级内容
            page = page.replace('&detail', case_detail)
            # 以写模式创建以版本信息和测试日期为名称的html失败的测试用例报告
            with open(f'{report_path}/{m}12.html', 'w',encoding='utf8') as f:
                f.write(page)
            # 替换html测试报告的table模块级内容
        s = s.replace('&detail', detail)

        # 生成完整测试报告
        if not os.path.exists(f'{report_path}/{version}'):  # 判断目录是否存在
            os.system(f'mkdir {report_path}/{version}')  # 新建目录，目录名为版本号
        with open(f'{report_path}/{version}.html', 'w',encoding='utf8') as f:
            f.write(s)




# obj = None
# for i in files:
#     data = read_csv(os.path.join(data_path,i))[1:]
#     obj = eval('Test_' + data[0][1].capitalize() + '()')
#     # if 'login' in data[0][1]:
#     #     obj = Test_Login()
#     # elif 'add_customer' in data[0][1]:
#     #     obj = Test_Add_customer()
#     for i in data:
#         obj.test(i)
#         time.sleep(2)
if __name__ == '__main__':
    # th1=threading.Thread(target=run,args=('火狐',))
    # th2=threading.Thread(target=run,args=('谷歌',))
    # th1.start()
    # th2.start()
    # run('火狐')
    report('v1.0','ui')



