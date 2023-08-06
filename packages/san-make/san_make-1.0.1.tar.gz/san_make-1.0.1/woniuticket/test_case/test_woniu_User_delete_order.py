import pytest
import requests
from woniuticket.coomon.common import get_data, get_dic, request_t
def setup_function():
    r1=request_t('get','http://192.168.255.180:14200/cinema-stage/admin/login',{'username':'小刘','password':'123456'})
    return r1
case=get_data(15)
@pytest.mark.parametrize('info',case['data'])
def test_main(info):
    data=get_dic(info[1])
    url=case['url']
    code=info[2]
    message=info[3]
    method=case['method']
    r=request_t(m=method,url=url,data=data)
    if code=='null':
        code=None
    if message=='null':
        message=None
    print(r.json())
    if code=='N/A':
        assert message in r.json()['message']
    elif message==None:
        assert code==r.json()['code']
    else:
        assert code == r.json()['code']
        assert message in r.json()['message']

def teardown_function():
    r1=request_t('delete','http://192.168.255.180:14200/api-user/user/userlogout')
if __name__ == '__main__':
    pytest.main(['-v',__file__])

