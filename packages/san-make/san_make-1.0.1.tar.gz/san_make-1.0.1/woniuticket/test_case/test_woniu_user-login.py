from woniuticket.coomon.common import get_data, get_dic, request_t
import pytest
case=get_data(14)
@pytest.mark.parametrize('info',case['data'])
def test_main1(info):
    if info[2]!='success':
        pytest.skip()
    else:
        data=get_dic(info[1])
        url='http://127.0.0.1:8080/woniusales/user/login'
        code=info[2]
        message=info[3]
        method=case['method']
        r=request_t(m=method,url=url,data=data)
        print(r.json())
        assert code in r.json()['code']
        assert message in r.json()['message']

# def teardown_function():
#     r=request_t('delete','http://192.168.255.180:14200/api-user/user/userlogout')
#     print(r.json())
#     return r

if __name__ == '__main__':
    pytest.main(['-v',__file__])
    # print(case)