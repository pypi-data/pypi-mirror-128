import pytest
# 使用pytest完成login、add_user、delete_user功能的测试
# add_user、delete_user功能需要登录后才能使用

def login(name='admin',passwd='123456'):
    if name == 'admin' and passwd == '123456':
        return 'success'
    else:
        return 'account or password error'

def add_user(id,name,pwd):
    if id not in ('1001','1002', '1003', '1004'):  # 判断id是否存在
        if name not in ('admin','admin1','admin2','admin3'):  # 判断用户名是否存在
            return 'add user success'
        return 'name already exists'
    else:
        return 'id already exists'

def delete_user(id):
    if id in ('1001','1002', '1003', '1004'):   # 判断id是否存在
        if id == '1001':    # 判断id是否为管理员
            return 'administrator cannot be deleted'
        else:
            return 'delete success'
    return 'id does not exists'
# def setup_function():
#     login('admin','12345q6')
#     print('测试开始')
# def teardown_function():
#     print('测试完成')
infos=[('1005','admin5','215361','pass'),('1004','admin5','215361','filed'),('1005','admin3','215361','filed'),('1002','admin2','215361','filed')]
@pytest.mark.parametrize('info',infos)
def test_1(q12,info):
    id,name,pwd,ex=info[0],info[1],info[2],info[3]
    a=add_user(id,name,pwd)
    if ex=='pass':
        assert 'success' in a
    else:
        assert  'exists' in a

infos1=[('1003','pass'),('1001','filed'),('1005','filed')]
@pytest.mark.parametrize('info',infos1)
def test_2(q12,info):
    id,ex=info[0],info[1]
    a=delete_user(id)
    if ex=='pass':
        assert 'success' in a
    else:
        assert  'not' in a


if __name__ == '__main__':
    pytest.main(['-s','./'])
    # pytest.main(['-v','-k k','test1.py'])
