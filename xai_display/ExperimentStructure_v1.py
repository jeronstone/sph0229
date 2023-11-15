import socket # To communicate with Baxter
from pynput import keyboard # To collect Button inputs
from ctypes import windll # To send triggers
import time # To send Triggers

# Trigger Names:
#1- VS done
#2- Policy done
#10 - Baxter's Turn
#20 - Human's Turn
#40 - red
#60 - green

def sendTrigger(val):
    pport = windll.inpoutx64
    pport.Out32(0xBFF8, 0) # sets all pins to low
    time.sleep(0.003)
    pport.Out32(0xBFF8, val) # sets pin no.1 to high
    time.sleep(0.003)
    pport.Out32(0xBFF8, 0) # sets all pins to low

def moveBaxter(curMP, nexMP, gripDir):
    message = ('[', curMP, ',', nexMP, ',', gripDir, ']')#"[117, 077, 0]"

    host = 'local host'
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', port))
    s.listen(1)
    c, addr = s.accept()
    info = s.getsockname()
    c.send(message.encode())
    c.close()

def buttonPress():
    with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('r'):
            print("Red")
            buttonVal = 40
            return buttonVal

        if event.key == keyboard.KeyCode.from_char('g'):
            print("Green")
            buttonVal = 60
            return buttonVal

def visualSystem():
    curState = [['I', 'I', '_', 'L', 'L','L', 'i'],
               ['J', 'J', '_', '_', 'b', '_', 'i'],
               ['k', '_', 'A', 'A', 'b', '_', 'h'],
               ['k', '_', '_', '_', 'b', '_', 'h'],
               ['k', '_', 'd', 'C', 'C', '_', 'g'],
               ['m', '_', 'd', '_', '_', '_', 'g'],
               ['m', '_', 'E', 'E', '_', 'F', 'F']]  #example
    return curState

def RushHourPolicy(curstate, method):
    if method == 1:
        # run with intermediate state X
    else: # method =2
        # run with intermediate state Y

    return curMP, nexMP, gripDir, xai, solvedState

def baxterTurn(method, xai, solvedState):

    # First check if it is solved:
    if solvedState == 1:
        state = 1
        #exit?
        return state

    # If Baxter's Turn:
    sendTrigger(10)

    # Run the visual system first:
    [ curState ] = visualSystem()
    sendTrigger(1)

    # Run the policy next:
    [ curMP, nexMP, gripDir, xai] = RushHourPolicy( curState, method )
    sendTrigger(2)

    # Run Baxter:
    moveBaxter(curMP, nexMP, dir)

    buttonVal = buttonPress()
    sendTrigger(buttonVal)

    # Show explanation:
    if not no exp:
        buttonVal = buttonPress()
        sendTrigger(buttonVal)

        get_random_policy()
        send_image(currMP.goodimage)
        sendtext(currMP.goodtext)

        
    else:
        pass
        # Show a blank screen with "Teammate completing turn" or something

    # How does this program know when Baxter is done moving?
    # Participant must press red when Baxter says done.
    buttonVal = buttonPress()
    sendTrigger(buttonVal)

    ###


def humanTurn():
    # If Human's Turn:
    sendTrigger(10)

    # Participant must press green to start turn
    buttonVal = buttonPress()
    sendTrigger(buttonVal)

    # Participant must press green to end turn
    buttonVal = buttonPress()
    sendTrigger(buttonVal)

## Initialize ##
Method = 1 # 1 or 2
    # What method? m1/m2
    # method1 - 1
    # method2 = 2
XAI = 1 # 1, 2, or 3
    # 1 - none
    # 2 - correct
    # 3 - incorrect

# Send inital trigger markers:
# m1 - no = 101
# m1 - cor = 102
# m1 - inc = 103
# m2 - no = 104
# m2 - cor = 105
# m2 - inc = 106
if Method ==1 & XAI == 1:
    intTrigger = 101
elif Method ==1 & XAI == 2:
    intTrigger = 102
elif Method ==1 & XAI == 3:
    intTrigger = 103
elif Method ==2 & XAI == 1:
    intTrigger = 104
elif Method ==2 & XAI == 2:
    intTrigger = 105
else: #Method ==2 & XAI == 3:
    intTrigger = 106
sendTrigger(intTrigger)

# To start, Participant must press red.
buttonVal = buttonPress()
sendTrigger(buttonVal)


state = 0 # unsolved
turnState = 1


while state == 0:
    # Keep taking turns until state = 1

    # Set turns
    if turnState == 1:
        state = baxterTurn(Method, XAI, state)
        turnState = 0
    else:
        humanTurn()
        turnState = 1

# Once it is solved, ask for final red button
buttonVal = buttonPress()
sendTrigger(buttonVal)





