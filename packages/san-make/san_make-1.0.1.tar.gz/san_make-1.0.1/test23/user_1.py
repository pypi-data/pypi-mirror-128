import socket
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip='192.168.11.222'
port=5321
soc.connect((ip,port))
str=input('shbash')
soc.send(str.encode('utf8'))