import socket,requests
from flask import Flask
soc=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
ip='192.168.11.222'
port=5321
soc.connect((ip,port))

msg=soc.recv(1024)
print(msg.decode('utf8'))