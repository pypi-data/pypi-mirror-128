import time

import websocket,json

url='ws://14.215.128.97:29316/'
ws=websocket.WebSocket()
ws.connect(url)
data={"type":"getGps"}
data2={"type":"getBitRate"}
data=json.dumps(data)
data2=json.dumps(data2)
ws.send(data)
time.sleep(1)
rev=ws.recv()
print(rev)
ws.send(data2)
time.sleep(1)
rev=ws.recv()
print(rev)
ws.close()

