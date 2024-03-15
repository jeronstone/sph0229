from XAIDisplay import *
from time import sleep

display = XAIDisplay()

sleep(5)

display.send_status(1)
display.send_image("./TM_01.png")
display.send_exp_text("This is [h]an explanation[h] of [h]the thing[h] above!")
sleep(5)
display.send_status(0)
display.send_image("./TM_02.png")
display.send_exp_text("this is [h]also an[h] explanation!")