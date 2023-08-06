import redis
con=redis.ConnectionPool(host='192.168.153.128',port=6379,db=0,decode_responses=True)
red=redis.Redis(connection_pool=con)
red.set('name','addmin')
red.hset('dic',key='adc',value='bc')
red.hmset('dic',mapping={'dad':'adad','adadad':'1231'})
print(red.get('name'))
print(red.hgetall('dic'))