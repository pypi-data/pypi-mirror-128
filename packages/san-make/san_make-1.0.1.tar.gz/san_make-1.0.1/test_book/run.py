import pytest,os
from test_book.common.utils import read_csv,data_bath,get_data,base_url,request,get_time,report_bath,case_bath
t=get_time()
pytest.main(['-v',f'--html={report_bath}/{t}.html',case_bath])


