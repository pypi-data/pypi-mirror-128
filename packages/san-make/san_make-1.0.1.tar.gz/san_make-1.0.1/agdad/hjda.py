import logging
import os

l=logging.getLogger()
l.setLevel(logging.INFO)
l_bath=os.path.join(os.path.dirname(__file__)+'/log/')
l_name=l_bath+'12.log'
f=logging.FileHandler(l_name,mode='a')
f.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
f.setFormatter(formatter)
l.addHandler(f)
l.debug('this is a logger debug message')
l.info('this is a logger info message')
l.warning('this is a logger warning message')
l.error('this is a logger error message')
l.critical('this is a logger critical message')



if __name__ == '__main__':
    print(l_bath)