from XAIDisplay import *
from time import sleep

display = XAIDisplay()

display.send_status(1)
display.send_image("./TM_01.png")
display.send_exp_text("explanation1")
sleep(5)
display.send_status(0)
display.send_image("./TM_02.png")
display.send_exp_text("explanation 2")