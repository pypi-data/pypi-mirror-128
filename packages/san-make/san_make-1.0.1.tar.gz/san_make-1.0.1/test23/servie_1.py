import socket,re
# soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# ip='192.168.11.222'
# port=5321
# soc.bind((ip,port))
# soc.listen(5)
# a,adress=soc.accept()
# a1,adress1=soc.accept()
# msg=a.recv(1024)
# msg=msg.decode('utf8')
# a1.send(msg.encode('utf8'))
s = '123!##a1sd12_as^&12789_asd9%&*'
r=re.findall('\d{2,}',s)
print(r)
r.sort(reverse=True)
print(r)
a=str.join(',',r)
a=re.sub(',','',a)
print(a)