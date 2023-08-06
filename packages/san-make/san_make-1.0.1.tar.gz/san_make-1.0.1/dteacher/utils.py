import random,time
class Utils:
    def is_continue(self):
        mark = input('继续输入请按1，结束请按任意键：')
        if mark == '1':
            return True
        return False
    def get_time(self):
        return time.strftime('%Y-%m-%d %X')
