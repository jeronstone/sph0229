import webbrowser
import os
#import websocket
from websocket_server import WebsocketServer
import json
import threading

tree_lut = [1,2,3]
ws_server: WebsocketServer

def get_turn_image(turn):
    return "local_im_{turn_num}.jpeg".format(turn_num=turn)

def get_turn_exp_fi(turn):
    return "local_txt_{turn_num}.txt".format(turn_num=turn)

#webbrowser.open(os.getcwd() + "/index.html")

try:
    ws_server=WebsocketServer(port=8888, host='')
except OSError as e:
    print(e)
    exit(1)

def new_client(client, server: WebsocketServer):
    print("new connection")
    send_info(1)

def send_info(current):
    to_send["image_link"] = get_turn_image(current)
    f = open(get_turn_exp_fi(current))
    to_send["text_raw"] = f.read()
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send")
    f.close()

ws_server.set_fn_new_client(new_client)
threading.Thread(target=ws_server.run_forever, name='Local Server', daemon=True).start()

to_send = {}

level=0
current=1

while(1):
    tree_in = input()
    level+=1
    current = 2**level + current
    if tree_in == "l":
        current-=1
    elif tree_in == "r":
        pass
    else:
        exit(1)
    send_info(current)
