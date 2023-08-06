import pytest
@pytest.fixture(name='q12',scope='package')
def login(name='admin',passwd='123456'):
    print('hghhvhv')
    if name == 'admin' and passwd == '123456':
        return 'success'
    else:
        return 'account or password error'