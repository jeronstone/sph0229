from Josh.sph0229.XAI_Project.XAI_Project_finals.XAIDisplay import *
from time import sleep

display = XAIDisplay()

sleep(5)

display.send_status("your turn")
display.send_image("./TM_01.png")
display.send_exp_text("This is [h]an explanation[h] of [h]the thing[h] above!")
sleep(5)
display.send_status("my turn")
display.send_image("./TM_02.png")
display.send_exp_text("this is [h]also an[h] explanation!")