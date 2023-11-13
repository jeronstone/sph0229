import webbrowser
import os
#import websocket
from websocket_server import WebsocketServer
import json
import threading
from time import sleep

ws_server: WebsocketServer

class Node:

    state=0
    children=[]

    def __init__(self, state, children):
        self.state = state
        self.children=children

    def get_turn_image(self):
        return "local_im_{turn_num}.jpeg".format(turn_num=self.state)

    def get_turn_exp_fi(self):
        return "local_txt_{turn_num}.txt".format(turn_num=self.state)
    
    def add_children(self, children):
        children += children

    def add_child(self, child):
        self.add_children([child])

    def remove_children(self, to_remove):
        for child in to_remove:
            if child in self.children:
                self.children.remove(child)

    def remove_child(self, to_remove):
        self.remove_children([to_remove])

curr=Node(0, [Node(1, [Node(3, []), Node(4, []), Node(5,[])]), Node(2, [Node(6,[])])])

try:
    ws_server=WebsocketServer(port=8888, host='')
except OSError as e:
    print(e)
    exit(1)

def new_client(client, server: WebsocketServer):
    print("new connection")
    if (curr.state>0):
        send_info()

to_send = {}

def send_info():
    to_send["op"] = "info"
    to_send["image_link"] = curr.get_turn_image()
    f = open(curr.get_turn_exp_fi())
    to_send["text_raw"] = f.read()
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send info")
    f.close()

def send_blank():
    to_send["op"] = "blank"
    to_send["image_link"] = "blank_focal.jpeg"
    to_send["text_raw"] = ""
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send blank")

ws_server.set_fn_new_client(new_client)
threading.Thread(target=ws_server.run_forever, name='Local Server', daemon=True).start()

webbrowser.open(os.getcwd() + "/index.html")

switch = 1

while(1):
    tree_in = input()
    if (switch == 0):
        if (tree_in != "r"):
            continue
        switch = 1
        send_blank()
    else:
        try:
            tree_in = int(tree_in)
        except:
            continue
        switch = 0
        curr=curr.children[tree_in]
        send_info()
