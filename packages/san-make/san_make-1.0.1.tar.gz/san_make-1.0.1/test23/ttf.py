import time,pytest
def time_1(func):
    print(func)
    def inner(*args,**kwargs):
        print(**kwargs)
        start=time.time()
        r=func(*args,**kwargs)
        end=time.time()
        print(end-start)
        return r
    return inner

@time_1
def f1(a):
    s=0
    for i in range(1,a+1):
        s+=i
    print(s)



if __name__ == '__main__':
    s1=f1(1000000)
    s2=f1(9999999)