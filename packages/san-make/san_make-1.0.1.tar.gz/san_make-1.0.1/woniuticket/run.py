import os
import time


from woniuticket.test_case import *
import pytest
base_path=os.path.dirname(__file__)
case_path=os.path.join(base_path,'test_case')
report_path=os.path.join(base_path,'report')
t=time.strftime('%Y%m%d-%H%M%S')
pytest.main(['-v',case_path])
# pytest.main(['-v','--alluredir=./report/',case_path])
# os.system('D:\\Programs\\allure-commandline-2.8.1\\allure-2.8.1\\bin\\allure.bat generate "D:\\python test\\woniuticket\\report"
# -o "D:\\python test\\woniuticket\\report\\alreport" ')
