
from websocket_server import WebsocketServer
import threading
import json
import webbrowser
import os
import random
from time import sleep

def new_client(client, server: WebsocketServer):
    pass

class XAIDisplay():

    ws_server: WebsocketServer

    def __init__(self):
        try:
            self.ws_server=WebsocketServer(port=8888, host='')
        except OSError as e:
            print(e)
            exit(1)
        self.ws_server.set_fn_new_client(new_client)
        threading.Thread(target=self.ws_server.run_forever, name='Local Server', daemon=True).start()
        webbrowser.open(os.getcwd() + "/index.html")
        sleep(1)
    
    def send_image_and_text(self, image, text):
        to_send = {}
        to_send["op"] = "imgntxt"
        to_send["image_link"] = image
        to_send["text_raw"] = text
        self.send_to_display(to_send)

    def send_image(self, image):
        to_send = {}
        to_send["op"] = "img"
        to_send["image_link"] = image
        self.send_to_display(to_send)

    def send_exp_text(self, text):
        to_send = {}
        to_send["op"] = "txt"
        to_send["text_raw"] = text
        self.send_to_display(to_send)
        
    def send_status(self, turn):
        to_send = {}
        to_send["op"] = "status"
        if (turn == 0):
            to_send["text_status"] = "Your Turn"
        else:
            to_send["text_status"] = "My Turn"
    
        self.send_to_display(to_send)

    def send_to_display(self, to_send):
        for client in self.ws_server.clients:
            self.ws_server.send_message(client, json.dumps(to_send))

# todo probably move this
# policy probs
prob_good = .3
prob_okay = .4
prob_bad = .3

def get_random_policy():
    prob = random.random()
    if (prob < prob_good):
        doc="g"
    elif (prob-prob_good < prob_okay):
        doc="o"
    else:
        doc="b"
    return doc