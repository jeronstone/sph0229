import webbrowser
import os
#import websocket
from websocket_server import WebsocketServer
import json
import threading
from time import sleep
import random

# True for debug prints
# False for no debug prints
LOUD=False

ws_server: WebsocketServer

# policy probs
prob_good = .3
prob_okay = .4
prob_bad = .3

processing_delay = 3 # seconds

turn = 0    # 0 your turn
            # 1 my turn

# generates random policy
doc = "g"
def rand_doc():
    prob = random.random()
    if (LOUD):
        print("prob " + str(prob))
    if (prob < prob_good):
        doc="g"
    elif (prob-prob_good < prob_okay):
        doc="o"
    else:
        doc="b"
    if (LOUD):
        print("policy " + doc)
    return doc

# Tree nodes
class Node:

    state=0
    children=[]

    def __init__(self, state, children):
        self.state=state
        self.children=children

    def get_turn_image(self, doc):
        return "{turn_num}_{policy}.jpeg".format(turn_num=self.state, policy=doc)

    def get_turn_exp_fi(self, doc):
        return "{turn_num}_{policy}.txt".format(turn_num=self.state, policy=doc)
    
    def add_children(self, children):
        self.children += children

    def add_child(self, child):
        self.add_children([child])

    def remove_children(self, to_remove):
        for child in to_remove:
            if child in self.children:
                self.children.remove(child)

    def remove_child(self, to_remove):
        self.remove_children([to_remove])

# generates dummy tree
# in below code, generates 99 nodes, assigns 3 children to each (if possible)
nodes = []
for i in range(0,100):
    nodes.append(Node(i,[]))

nodes[0].add_children([nodes[1],nodes[2],nodes[3]])

for i in range(100,0,-1):
    try:
        nodes[i].add_children([nodes[3*i+1],nodes[3*i+2],nodes[3*i+3]])
    except:
        continue

if (LOUD):
    for node in nodes:
        print("node: " + str(node.state))
        print("children: ")
        for child in node.children:
            print(child.state)

curr=nodes[0]

# define websocket server
try:
    ws_server=WebsocketServer(port=8888, host='')
except OSError as e:
    print(e)
    exit(1)

# runs when a new webpage is loaded
def new_client(client, server: WebsocketServer):
    print("new connection")
    if (curr.state>0):
        send_info()

# seperated due to op code overwrite due to threads
to_send_info = {}
to_send_status = {}

# sends image and explanation to webpage
def send_info(delay):
    sleep(delay)
    to_send_info["op"] = "info"
    doc = rand_doc()
    to_send_info["image_link"] = curr.get_turn_image(doc)
    f = open(curr.get_turn_exp_fi(doc))
    to_send_info["text_raw"] = f.read()
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send_info))
    if (LOUD):
        print("ws send info")
        print(to_send_info)
    f.close()

# sends blank (focal point) and no text to webpage
def send_blank(delay):
    sleep(delay)
    to_send_info["op"] = "info"
    to_send_info["image_link"] = "blank_focal.jpeg"
    to_send_info["text_raw"] = ""
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send_info))
    if (LOUD):
        print("ws send blank")
        print(to_send_info)

# updates my turn / your turn / processing... status on webpage
def send_status(delay, status):
    sleep(delay)
    to_send_status["op"] = "status"
    to_send_status["text_status"] = status
    for client in ws_server.clients:
        ws_server.send_message(client, json.dumps(to_send_status))
    if (LOUD):
        print("ws send status")
        print(to_send_status)

# start server
ws_server.set_fn_new_client(new_client)
threading.Thread(target=ws_server.run_forever, name='Local Server', daemon=True).start()

# auto open page
webbrowser.open(os.getcwd() + "/index.html")

# input loop
while(1):
    # turn 0 = your turn
    if (turn == 0):

        # wait for red button
        button_in = input()
        if (button_in != "r"):
            continue
        if (LOUD):
            print("red (r) button pressed")

        # wait for number to specify which child of tree to go to (automated in reality)
        tree_in = input()
        try:
            tree_in = int(tree_in)
        except:
            continue

        # update status and switch to my turn
        # will spawn threads to create processing delay effect
        turn = 1
        send_status(0, "Processing...")
        curr=curr.children[tree_in]
        x = threading.Thread(target=send_info, args=(processing_delay,))
        x.start()
        y = threading.Thread(target=send_status, args=(processing_delay,"My Turn"))
        y.start()

    # turn 1 = my turn
    if (turn == 1):

        # wait for any input for now to continue (automated in reality (i think))
        button_in = input()
        turn = 0
        send_blank(0)
        send_status(0, "Your Turn")
