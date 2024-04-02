from XAIDisplay import *
from time import sleep

display = XAIDisplay()

sleep(1)

display.send_status("your turn")
display.send_image("/home/jstone14/sph0229/XAI_Project/xai_display/TM_01.png")
display.send_exp_text("This is [h]an explanation[h] of [h]the thing[h] above!")
display.update_progress(80)
sleep(5)
display.send_status("my turn")
display.send_image("/home/jstone14/sph0229/XAI_Project/xai_display/TM_02.png")
display.send_exp_text("this is [h]also an[h] explanation!")
display.update_progress(45)