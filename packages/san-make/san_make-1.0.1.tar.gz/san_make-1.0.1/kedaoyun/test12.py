#cording=utf8
import requests,pytest
url='http://127.0.0.1/?user/loginSubmit'
p={'name':'admin','password':'Zz123456','isAjax':'1','getToken':'1'}
r=requests.get(url=url,params=p).json()  #获取accessToken

# url='http://127.0.0.1/?explorer/pathList'
# p1={'accessToken':r['data']}
# r1=requests.post(url,p1)
# # print(r1.json())
#
# url='http://127.0.0.1/?explorer/pathInfo'
# p2={'dataArr':[{"type":"file","path":"D:/xampp/htdocs/data/User/admin/home/音乐/"}],'accessToken':r['data']}
# r2=requests.post(url,p2)
# # print(r2.json())

data=([r['data'],'D:/xampp/htdocs/data/User/admin/home/desktop/myfolder','True'],[r['data'],'','False'])
@pytest.mark.parametrize('info',data)
def test_mkdir(info):#新建文件夹接口测试
    url='http://127.0.0.1/?explorer/mkdir'
    p3={'accessToken':info[0],'path':info[1]}
    r3=requests.post(url,p3).json()
    assert info[-1]==str(r3['code'])

if __name__ == '__main__':
    pytest.main(['-v',__file__])