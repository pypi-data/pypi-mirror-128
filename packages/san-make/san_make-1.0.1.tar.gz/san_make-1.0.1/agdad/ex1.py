# *_* coding:utf-8 *_*
from websocket import ABNF
import json,_thread,time,websocket

class Api_Websocket_Test:

    def __init__(self,netPort,netIp='14.215.128.97'):
        self.url = f'ws://{netIp}:{netPort}/'

    @staticmethod
    def wsMessage(ws,message):
       print(message)

    @staticmethod
    def wsError(ws,error):
        return error

    @staticmethod
    def wsClose(ws,msg='close connection'):
        return msg

    @staticmethod
    def parmas(data):
        def wsOpen(ws):
            def run(*args):
                #content = args
                for i in data:
                    ws.send(json.dumps(i))
                # step = 3200
                # with open(wav_path,'rb') as f:
                #     while True:
                #         read_data = f.read(step)
                #         if read_data:
                #             ws.send(read_data, ABNF.OPCODE_BINARY)
                #         if len(read_data) < step:
                #             break
                #         time.sleep(0.1)
                # ws.send('', ABNF.OPCODE_BINARY)
                time.sleep(1)
                ws.close()
            _thread.start_new_thread(run,())
        return wsOpen



if __name__ == "__main__":
    #websocket.enableTrace(True)
    sock = Api_Websocket_Test(netPort=29320)
    ws = websocket.WebSocketApp(sock.url,on_message=sock.wsMessage,on_error=sock.wsError,on_close=sock.wsClose)
    data = {"type": "getGps"}
    data2 = {"type": "getBitRate"}
    l=[data,data2]
    ws.on_open = sock.parmas(l)
    ws.run_forever()

