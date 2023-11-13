import webbrowser
import os
#import websocket
from websocket_server import WebsocketServer
import json
import threading
from time import sleep
import random

ws_server: WebsocketServer

prob_good = .3
prob_okay = .4
prob_bad = .3
processing_delay = 1 # seconds

turn = 0    # 0 your turn
            # 1 my turn

doc = "g"

def rand_doc():
    prob = random.random()
    print(prob)
    if (prob < prob_good):
        doc="g"
    elif (prob-prob_good < prob_okay):
        doc="ok"
    else:
        doc="b"
    print(doc)
    return doc

class Node:

    state=0
    children=[]

    def __init__(self, state, children):
        self.state = state
        self.children=children

    def get_turn_image(self, doc):
        return "local_im_{turn_num}_{doctrine}.jpeg".format(turn_num=self.state, doctrine=doc)

    def get_turn_exp_fi(self, doc):
        return "local_txt_{turn_num}_{doctrine}.txt".format(turn_num=self.state, doctrine=doc)
    
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

def send_info(delay):
    sleep(delay)
    to_send["op"] = "state"
    doc = rand_doc()
    to_send["image_link"] = curr.get_turn_image(doc)
    f = open(curr.get_turn_exp_fi(doc))
    to_send["text_raw"] = f.read()
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send info")
    f.close()

def send_blank(delay):
    sleep(delay)
    to_send["op"] = "state"
    to_send["image_link"] = "blank_focal.jpeg"
    to_send["text_raw"] = ""
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send blank")

def send_status(delay, status):
    sleep(delay)
    to_send["op"] = "status"
    to_send["text_status"] = status
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send))
    print("ws send status")

ws_server.set_fn_new_client(new_client)
threading.Thread(target=ws_server.run_forever, name='Local Server', daemon=True).start()

webbrowser.open(os.getcwd() + "/index.html")

while(1):
    if (turn == 0):
        button_in = input()
        if (button_in != "r"):
            continue
        tree_in = input()
        try:
            tree_in = int(tree_in)
        except:
            continue

        turn = 1
        send_status(0, "Processing...")
        curr=curr.children[tree_in]
        x = threading.Thread(target=send_info, args=(processing_delay,))
        x.start()
        y = threading.Thread(target=send_status, args=(processing_delay,"My Turn"))
        y.start()
    if (turn == 1):
        button_in = input()
        turn = 0
        send_blank(0)
        send_status(0, "Your Turn")
