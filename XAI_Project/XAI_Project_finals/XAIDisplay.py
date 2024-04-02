
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

        self.xai_highlight_delimiter = "[h]"

        self.ws_server.set_fn_new_client(new_client)
        threading.Thread(target=self.ws_server.run_forever, name='Local Server', daemon=True).start()

        webbrowser.open('/home/jstone14/sph0229/XAI_Project/XAI_Project_finals/index.html')
        sleep(1)

    def delimiter_to_mark(self, text):
        temp = text.split(self.xai_highlight_delimiter)
        print(temp)
        prepost = ""
        for i in range(len(temp)-1):
            temp[i] = temp[i]+"<"+prepost+"mark>"
            prepost = "/" if prepost == "" else ""
        return "".join(temp)
    
    def send_image_and_text(self, image, text):
        to_send = {}
        to_send["op"] = "imgntxt"
        to_send["image_link"] = image
        to_send["text"] = self.delimiter_to_mark(text)
        self.send_to_display(to_send)

    def send_image(self, image):
        to_send = {}
        to_send["op"] = "img"
        to_send["image_link"] = image
        self.send_to_display(to_send)

    def send_exp_text(self, text):
        to_send = {}
        to_send["op"] = "txt"
        to_send["text"] = self.delimiter_to_mark(text)
        self.send_to_display(to_send)
        
    def send_status(self, msg):
        to_send = {}
        to_send["op"] = "status"    
        to_send["text_status"] = msg
        self.send_to_display(to_send)

    def update_progress(self, prog):
        to_send = {}
        to_send["op"] = "progress"
        to_send["prog_num"] = str(prog)
        self.send_to_display(to_send)

    def send_to_display(self, to_send):
        # just send it to all clients - should only be one
        for client in self.ws_server.clients:
            self.ws_server.send_message(client, json.dumps(to_send))

# TODO: old I think?
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