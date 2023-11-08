import webbrowser
import os
#import websocket
from websocket_server import WebsocketServer
import json
import threading
from time import sleep

ws_server: WebsocketServer

def get_turn_image(turn):
    return "local_im_{turn_num}.jpeg".format(turn_num=turn)

def get_turn_exp_fi(turn):
    return "local_txt_{turn_num}.txt".format(turn_num=turn)


current=0

try:
    ws_server=WebsocketServer(port=8888, host='')
except OSError as e:
    print(e)
    exit(1)

def new_client(client, server: WebsocketServer):
    print("new connection")
    if (current>0):
        send_info(current)

def send_info(current):
    to_send["image_link"] = get_turn_image(current)
    f = open(get_turn_exp_fi(current))
    to_send["text_raw"] = f.read()
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send 1 ")
    # sleep(5)
    # to_send['image_link'] = "done"
    # to_send["text_raw"] = f.read()
    # for client in ws_server.clients:
    #     ws_server.send_message(client, json.dumps(to_send))
    # print("ws send 2")
    f.close()

ws_server.set_fn_new_client(new_client)
threading.Thread(target=ws_server.run_forever, name='Local Server', daemon=True).start()

webbrowser.open(os.getcwd() + "/index.html")

to_send = {}

while(1):
    tree_in = input()
    current = 2*current+1
    if tree_in == "l":
        pass
    elif tree_in == "r":
        current+=1
    else:
        exit(1)
    print(current)
    send_info(current)
