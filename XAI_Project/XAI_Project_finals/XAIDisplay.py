
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
        # initialze websocket server
        # when html file is opened, javascript on the page will "connect" to this python script via localhost
        try:
            self.ws_server=WebsocketServer(port=8888, host='')
        except OSError as e:
            # failed to connect
            print(e)
            exit(1)

        # set delimiter for highlighted text for xai text
        self.xai_highlight_delimiter = "[h]"

        # begin websocket connection in new thread
        self.ws_server.set_fn_new_client(new_client)
        threading.Thread(target=self.ws_server.run_forever, name='Local Server', daemon=True).start()

        # open browser to html file
        webbrowser.open('C:/Users/SPH0229/Documents/BaxterCV/XAI_Project/Explanations/sph0229/XAI_Project/XAI_Project_finals/index.html')
        sleep(1)

    # converts delimiter in text (defined in init) to <mark> for html
    def delimiter_to_mark(self, text):
        temp = text.split(self.xai_highlight_delimiter)
        prepost = ""
        for i in range(len(temp)-1):
            temp[i] = temp[i]+"<"+prepost+"mark>"
            prepost = "/" if prepost == "" else ""
        return "".join(temp)
    
    # sends image with explanation at the same time
    # not any different than sending individually other than it will change the text/image closer together time wise (aka it is faster)
    def send_image_and_text(self, image, text):
        to_send = {}
        to_send["op"] = "imgntxt"
        to_send["image_link"] = image
        to_send["text"] = self.delimiter_to_mark(text)
        self.send_to_display(to_send)

    # updates xai image with image found at param path
    def send_image(self, image):
        to_send = {}
        to_send["op"] = "img"
        to_send["image_link"] = image
        self.send_to_display(to_send)

    # updates explanation text box with parameter text
    def send_exp_text(self, text):
        to_send = {}
        to_send["op"] = "txt"
        to_send["text"] = self.delimiter_to_mark(text)
        self.send_to_display(to_send)
        
    # update the "status" bar (top of the page)
    # call this with the string you want to send
    def send_status(self, msg):
        to_send = {}
        to_send["op"] = "status"    
        to_send["text_status"] = msg
        self.send_to_display(to_send)

    # update value of progress bar - unused, there's no progress bar
    # def update_progress(self, prog):
    #     to_send = {}
    #     to_send["op"] = "progress"
    #     to_send["prog_num"] = str(prog)
    #     self.send_to_display(to_send)

    # internal use function to send messages to websocket client
    def send_to_display(self, to_send):
        # just send it to all clients - should only be one anyways
        for client in self.ws_server.clients:
            self.ws_server.send_message(client, json.dumps(to_send))


# randomly select correct, subtle incorrect, or obvious incorrect
def get_random_policy():
    # policy probs
    prob_correct = .16
    prob_subtle = .42
    prob_obvious = .42

    prob = random.random()
    if (prob < prob_correct):
        doc="11"
    elif (prob-prob_correct < prob_subtle):
        doc="13"
    else:
        doc="12"
    return doc