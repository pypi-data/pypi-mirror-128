import os

from woniuticket.coomon.common import get_data, get_dic, request_t
import pytest
case=get_data(7)
@pytest.mark.parametrize('info',case['data'])
def test_main(info):
    data=get_dic(info[1])
    url=case['url']
    code=info[2]
    message=info[3]
    method=case['method']
    r=request_t(m=method,url=url,data=data)
    print(r.json())
    assert code in r.json()['code']
    assert message in r.json()['message']
case=get_data(0)
@pytest.mark.parametrize('info',case['data'])
def test_main1(info):
    data=get_dic(info[1])
    url=case['url']
    print(url)
    code=info[2]
    message=info[3]
    method=case['method']
    r=request_t(m=method,url=url,data=data)
    print(r.json())
    assert code in r.json()['code']
    assert message in r.json()['message']

if __name__ == '__main__':
    pytest.main(['-v','--alluredir=../report/',__file__])
    # os.system('D:\\Programs\\allure-commandline-2.8.1\\allure-2.8.1\\bin\\allure.bat generate "D:\\python test\\woniuticket\\report" -o "D:\\python test\\woniuticket\\report\\alreport" ')

