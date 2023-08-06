import random,time
class Utils:
    def is_continue(self):
        mark = input('继续输入请按1，结束请按任意键：')
        if mark == '1':
            return True
        return False
    def get_time(self):
        return time.strftime('%Y-%m-%d %X')
if __name__ == '__main__':
    str='0123456789'
    print(28%10,str[1:5],str.index('12'),str.split('1'))
    l=[1,2,3,4,1]
    s='0'
    print(s.join('1212'),l[2:5])
    l.sort(reverse=False)
    print(list(str),l)
