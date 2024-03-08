import socket # To communicate with Baxter
from pynput import keyboard # To collect Button inputs
from ctypes import windll # To send triggers
import time # To send Triggers

# VS
import VisualSystem.VisualSystemCode
# Policy
import Policy.RHPolicy
import Policy.PolicyToGoal
import Policy.PolicyToHalf
# XAI
from Policy.PolicyToGoal import board_str
from difflib import SequenceMatcher
# Movement

# Josh imports
import XAIDisplay #TODO change path
from state_to_im import get_im_from_state #TODO change path

display = None

def sendTrigger(val):
    pport = windll.inpoutx64
    pport.Out32(0xBFF8, 0) # sets all pins to low
    time.sleep(0.003)
    pport.Out32(0xBFF8, val) # sets pin no.1 to high
    time.sleep(0.003)
    pport.Out32(0xBFF8, 0) # sets all pins to low

def buttonPress():
    with keyboard.Events() as events:
        # Block for as much as possible
        event = events.get(1e6)
        if event.key == keyboard.KeyCode.from_char('r'):
            print("Red")
            buttonVal = 114
            return buttonVal

        if event.key == keyboard.KeyCode.from_char('g'):
            print("Green")
            buttonVal = 103
            return buttonVal



# Baxter Functions: VS, Policy, XAI, Movement, Turn
def Pos2MP(Pos, BL):

    # Direction:
    r1 = Pos[0][0]
    r2 = Pos[1][0]
    if r1 == r2:
        #print('moved horizontally')
        dir = 0
    else:
        #print('moved vertically')
        dir = 1

    # Set the MP based on direction and position
    # Option 1: vert and long
    if dir == 1 and BL >2:
        #print('vert and long')
        Col, Row = Pos[0][1], Pos[1][0]
        #print('Center: (R, C) ', Row, Col)

        if Col == 0:
            colOpt = [1,21,41,61,81,101,121]
        elif Col == 1:
            colOpt = [3,23,43,63,83,103,123]
        elif Col == 2:
            colOpt = [5,25,45,65,85,105,125]
        elif Col == 3:
            colOpt = [7,27,47,67,87,107,127]
        elif Col == 4:
            colOpt = [9,29,49,69,89,109,129]
        elif Col == 5:
            colOpt = [11,31,51,71,91,111,131]
        elif Col == 6:
            colOpt = [13,33,53,73,93,113,133]

        MP = colOpt[Row]
    # Option 2: horz and long
    elif dir == 0 and BL >2:
        #print('horz and long')
        Col, Row = Pos[1][1], Pos[0][0]
        #print('Center: (R, C) ', Row, Col)

        if Row == 0:
            rowOpt = [1,3,5,7,9,11,13]
        elif Row == 1:
            rowOpt = [21,23,25,27,29,31,33]
        elif Row == 2:
            rowOpt = [41,43,45,47,49,51,53]
        elif Row == 3:
            rowOpt = [61,63,65,67,69,71,73]
        elif Row == 4:
            rowOpt = [81,83,85,87,89,91,93]
        elif Row == 5:
            rowOpt = [101,103,105,107,109,111,113]
        elif Row == 6:
            rowOpt = [121,123,125,127,129,131,133]

        MP = rowOpt[Col]
    # Option 3: vert and short
    if dir == 1 and BL == 2:
        #print('vert and short')
        Row1, Row2 = Pos[0][0], Pos[1][0]
        HL = (Row1 + Row2)/2 - 0.5
        Col = Pos[0][1]
        #print('Center: (HL, C) ', HL, Col)

        if HL == 0:
            HLOpt = [14,15,16,17,18,19,20]
        elif HL == 1:
            HLOpt = [34,35,36,37,38,39,40]
        elif HL == 2:
            HLOpt = [54,55,56,57,58,59,60]
        elif HL == 3:
            HLOpt = [74,75,76,77,78,79,80]
        elif HL == 4:
            HLOpt = [94,95,96,97,98,99,100]
        elif HL == 5:
            HLOpt = [114,115,116,117,118,119,120]

        MP = HLOpt[Col]
    # Option 4: horz and short
    elif dir == 0 and BL == 2:
        #print('horz and short')
        Col1, Col2 = Pos[0][1], Pos[1][1]
        VL = (Col1 + Col2) / 2 - 0.5
        Row = Pos[0][0]
        #print('Center: (R, VL) ', Row, VL)
        if VL == 0:
            VLOpt = [2,22,42,62,82,102,122]
        elif VL == 1:
            VLOpt = [4,24,44,64,84,104,124]
        elif VL == 2:
            VLOpt = [6,26,46,66,86,106,126]
        elif VL == 3:
            VLOpt = [8,28,48,68,88,108,128]
        elif VL == 4:
            VLOpt = [10,30,50,70,90,110,130]
        elif VL == 5:
            VLOpt = [12,32,52,72,92,112,132]

        MP = VLOpt[Row]

    return MP, dir

def setCorrect(route_start_goal):
    currentState = route_start_goal[0][0]
    current = board_str(currentState)
    nextState = route_start_goal[0][1]
    next = board_str(nextState)
    return current, next

def pickErrorOptions(route_start_goal, cost_node):

    #print(cost_node)
    #print(' ')
    currentState = route_start_goal[0][0]
    current = board_str(currentState)
    nextState = route_start_goal[0][1]
    next = board_str(nextState)
    #print(next)
    #print(' ')

    # Go through the cost dictionary
    similarity_cur = []
    similarity_nex = []
    for index, key in enumerate(cost_node):
        # find the N+1 (current state to next possible states) in the dictionary
        nextOptionLevel = float(cost_node[key])


        if nextOptionLevel == 2:
            #print("This state is one of the next state possibilities:")
            #print(key)
            nextOptions = key

            #https: // miguendes.me / python - compare - strings

            #print("Difference from current state:")
            #print(SequenceMatcher(a=nextOptions, b=current).ratio())
            fromCur = SequenceMatcher(a=nextOptions, b=current).ratio()

            #print("Difference from next state:")
            #print(SequenceMatcher(a=nextOptions, b=next).ratio())
            fromNex = SequenceMatcher(a=nextOptions, b=next).ratio()

            similarity_cur.append(fromCur)
            similarity_nex.append(fromNex)


            # Find the chosen next state
            #f fromNex == 1:
                #print(index)


    #print("Difference from next state:")
    #print(similarity_nex)

    # Find obvious error:
    maxDifference = min(similarity_nex)
    # Find subtle error:
    minDifference = sorted(similarity_nex)[-2]

    for index, key in enumerate(cost_node):
        # find the N+1 (current state to next possible states) in the dictionary
        nextOptionLevel = float(cost_node[key])
        if nextOptionLevel == 2:
            nextOptions = key
            fromNex = SequenceMatcher(a=nextOptions, b=next).ratio()

            # Pick the maximal difference from next state
            if fromNex == maxDifference:
                #print("Maximal difference from next state:")
                obviousError = nextOptions
                #print(obviousError)

            # Pick the minimal difference from next state
            if fromNex == minDifference:
                #print("Minimal difference from next state:")
                subtleError = nextOptions
                #print(subtleError)

    #print(' ')
    return obviousError, subtleError

def moveBaxter(curMP_val, nexMP_val, gripDir):
    #message = ('[', curMP, ',', nexMP, ',', gripDir, ']') #"[117, 077, 0]"
    curMP_str = str(curMP_val)
    if curMP_val<100:
        curMP = str(0)+str(curMP_str)
    else:
        curMP = str(curMP_str)

    nexMP_str = str(nexMP_val)
    if nexMP_val<100:
        nexMP = str(0)+str(nexMP_str)
    else:
        nexMP = str(nexMP_str)


    message = "[" + curMP + "," + nexMP + "," + str(gripDir) + "]"
    print(message)


    # Uncomment when ready to implement with Baxter moving:
    # host = 'local host'
    # port = 5000
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind(('', port))
    # s.listen(1)
    # c, addr = s.accept()
    # info = s.getsockname()
    # c.send(message.encode())
    # c.close()

def XAI(route_start_goal, cost_node, turnCounter, xaiTurn, xaiCondition):

    # Set participant understanding flag
    understandFlag = 0

    # No explanation
    if xaiCondition == 1:
        understandFlag = 1
        pass
    
    # Explanation givenr
    else:

        # If explanation is bad, pick the type from the pre-set array: correct/subtle-incorrect/obvious-incorrect
        if xaiCondition == 3:
            xaiType = xaiTurn[turnCounter-1]

            # Find XAI info:
            obvErr, subtErr = pickErrorOptions(route_start_goal, cost_node)
            # This is NOT perfect. Sometimes the obvious error is just an undo of the last move. May need to tweak this.

        else:
            xaiType = 11

            # Find XAI info:
            cur, nex = setCorrect(route_start_goal)

        # Correct explanation
        if xaiType == 11:
            # Display correct XAI **************************************************
            explanation = "cool and swag"
            display.send_image_and_text(get_im_from_state(cur, nex), explanation)
            print("Correct current to Next:")
            print(cur, nex)
            print(" ")
        elif xaiType == 12:
            # Display obvious incorrect XAI **************************************************
            explanation = "less cool and less swag"
            display.send_image_and_text(get_im_from_state(obvErr, cur), explanation)
            print("Obvious Error:")
            print(obvErr)
            print(" ")
        else:
            # Display subtle incorrect XAI **************************************************
            explanation = "less cool and still swag"
            display.send_image_and_text(get_im_from_state(subtErr, cur), explanation) 
            print("Subtle Error:")
            print(subtErr)
            print(" ")


    return understandFlag


def baxterTurn(solvedFlag, xaiTurn, turnCounter, beentoHalf, halfwayState):

    # First check if it is solved - this shouldn't be 0 coming in:
    if solvedFlag == 1:
        return 

    # Run VS to get current state:
    inputFromVS = [['C', 'C', 'C', 'i', 'D', 'D', 'D'],  # 2
                       ['m', 'B', 'B', 'i', 'j', 'k', 'l'],
                       ['m', 'A', 'A', 'i', 'j', 'k', 'l'],
                       ['m', 'E', 'E', '_', 'F', 'F', 'l'],
                       ['G', 'G', 'G', '_', '_', '_', '_'],
                       ['_', 'n', 'o', '_', '_', '_', '_'],
                       ['_', 'n', 'o', 'H', 'H', '_', '_']]          # VisualSystem.VisualSystemCode.main()
    print(inputFromVS)

    # Check if it is solved:
    solvedState = 0  # Assume unsolved to enter while loop
    BLANK = '_'
    ESCAPE_BLOCK = 'A'
    while solvedState != 1:
        # 1: Check if sovled
        char_i = inputFromVS[2][6]  # position next to the gate
        if char_i == BLANK:  # if it is a blank, it isn't solved
            print('blank space')
            solvedState = 0
        elif char_i == ESCAPE_BLOCK:  # if it is the exit bloc, it is solved
            print('exiting while loop')
            solvedState = 1 # policy
            solvedFlag = 1 # general
            pass
        else:  # if it is another block, it isn't solved
            print('another block')
            solvedState = 0


        # If it isn't solved, start Baxter turn:
        # Increase turn by 1
        turnCounter +=1 
        
        # Display: "My Turn"  **************************************************
        display.send_status("My Turn")

        # Send interanal start turn trigger:
        sendTrigger(101)    
        
        # Run the policy next:
        route_start_goal, cost_node, beentoHalf, halfwayState = Policy.RHPolicy.main(inputFromVS, beentoHalf, halfwayState)
        solvedState = 1
    print('Policy SOLVED')
    print(" ")

    # Get current and next state and their motor primitives:
    if len(route_start_goal[0]) == 1:
        "Goal state was the input. Exiting...."
        return
    else:
        currentState = route_start_goal[0][0]

        print("Current State:")
        print(currentState)
        nextState = route_start_goal[0][1]
        print("Next State:")
        print(nextState)
        print(' ')
        # Build an array of the locations
        # current
        blockPos_input = []
        for arrNum in enumerate(currentState):
            for position in enumerate(arrNum[1]):
                blockPos_input.append([arrNum[0], position[0], position[1]])
        # next
        blockPos_next = []
        for arrNum in enumerate(nextState):
            for position in enumerate(arrNum[1]):
                blockPos_next.append([arrNum[0], position[0], position[1]])

        # Where it was
        curMove = []
        for element in blockPos_next:
            if element not in  blockPos_input and element[2] != '_':
                curMove.append(element)
        #print('cur positions:',curMove)

        # What moved:
        letterMoved = curMove[0][2]
        print('letter moved: ', letterMoved)

        # Count how many exist in the current array
        blockLength = 0
        curLoc = []
        for arrNum in enumerate(currentState):
            for position in enumerate(arrNum[1]):
                if position[1] == letterMoved:
                    blockLength = blockLength+1
                    curLoc.append([arrNum[0],position[0]])
        nexLoc = []
        for arrNum in enumerate(nextState):
            for position in enumerate(arrNum[1]):
                if position[1] == letterMoved:
                    nexLoc.append([arrNum[0], position[0]])

        curMP, gripDir = Pos2MP(curLoc, blockLength)
        nexMP, gripDir = Pos2MP(nexLoc, blockLength)


        print('cur MP:', curMP)
        print('nex MP:', nexMP)


    # Move Baxter:
    # gripDir = 0 - horizontal
    # gripDir = 1 - vertical
    moveBaxter(curMP, nexMP, gripDir)


    # Check that participant is paying attention to Baxter moving:
    # Participant must press GREEN at start of movement
    print("Press GREEN")
    buttonVal = buttonPress()
    # Check for correctness
    if buttonVal == 114: 
        # Ask for correct button press
        # Display: "I moved, press the green button."  **************************************************
        display.send_status("I moved, press the green button.")

        # Look for button again
        print("Wrong button. Press GREEN")
        buttonVal = buttonPress()
    sendTrigger(buttonVal)

    
    # Wait for Baxter to place the block
    # This is an average movement time, for testing, this is set low
    time.sleep(3)
    

    # XAI 
    understandFlag = XAI(route_start_goal, cost_node, turnCounter, xaiTurn, xaiCondition)
    
    # Participant must confirm understanding before continuing
    if understandFlag == 0:
        # Participant must press RED to accept understanding
        print("Press RED")
        buttonVal = buttonPress()
        # Check for correctness
        if buttonVal == 103: 
            # Ask for correct button press
            # Display: "Check explanation, press the red button to confirm understanding."  **************************************************
            display.send_status('Check explanation, press the red button to confirm understanding.')

            # Look for button again
            print("Wrong button. Press RED")
            buttonVal = buttonPress()
        sendTrigger(buttonVal)

    # Send interanal end turn trigger:
    sendTrigger(101)


# Participant Functions: Turn
def humanTurn():
    # Send PT internal trigger to start turn:
    sendTrigger(100)

    # Participant must press GREEN to start turn
    buttonVal = buttonPress()
    # Check for correctness
    if buttonVal == 114: 
        # Ask for correct button press
        # Display: "Your Turn, press the green button to start turn."  **************************************************
        display.send_status("Your Turn, press the green button to start turn.")

        # Look for button again
        buttonVal = buttonPress()
    sendTrigger(buttonVal)



    # Participant must press RED to end turn
    buttonVal = buttonPress()
    # Check for correctness
    if buttonVal == 103: 
        # Ask for correct button press
        # Display: "Your Turn, press the red button to end turn."  **************************************************
        display.send_status("Your Turn, press the red button to end turn.")
        
        # Look for button again
        buttonVal = buttonPress()
    sendTrigger(buttonVal)

    # Send PT internal trigger to end turn:
    sendTrigger(100)



def main(xaiCondition, halfwayState, beentoHalf, solvedFlag, turnFlag, turnCounter, xaiTurn):

    # Send Initalization Trigger 
    # Value of condition
    sendTrigger(xaiCondition)


    # Display: "Ready to start?"  **************************************************
    display.send_status("Ready to start?")

    # To start, Participant must press RED.
    print("Press RED")
    buttonVal = buttonPress()
    sendTrigger(buttonVal)


    # Run through while loop until the task is solved
    # NOTE: This is a different flag from the solved flag used in the policy to exit the loop
    while solvedFlag == 0:

        # Baxter Turn:
        if turnFlag == 1:
            # My turn is not displayed yet not increased turn counter because the state of the board must check if solved.
            
            # Run Baxter turn:
            baxterTurn(solvedFlag, xaiTurn, turnCounter, beentoHalf, halfwayState)

            # Change turn flag to go to participant next
            turnFlag = 0

        # Participant Turn:
        else:
            # Increase turn by 1
            turnCounter +=1 

            # Display: "Your Turn"  **************************************************
            display.send_status("Your Turn")

            # Run Baxter turn:
            humanTurn()

            # Change turn flag to go to Baxter next
            turnFlag = 1



    # Display: "Task Complete?"  **************************************************
    display.send_status("Task Complete?")
            

    # Participant must press GREEN for agreement
    print("Press GREEN")
    buttonVal = buttonPress()
    # Check for correctness
    if buttonVal == 114: 
        # Ask for correct button press
        # Display: "Task Complete? Press the green button to complete."  **************************************************
        display.send_status("Task Complete? Press the green button to complete.")

        # Look for button again
        print("Wrong button. Press GREEN")
        buttonVal = buttonPress()
    sendTrigger(buttonVal)

    return xaiCondition, halfwayState, beentoHalf, solvedFlag, turnFlag, turnCounter, xaiTurn



if __name__ == '__main__':
    global halfwayState, beentoHalf


    # Inital Trial Settings:
    # 1. Explanation Condition
    # none = 1
    # good = 2
    # bad = 3
    xaiCondition = 1
    
    # Initialize display: **************************************************
    display = XAIDisplay()

    # If explanation is bad, determine which are correct(11)/subtle-incorrect(13)/obvious-incorrect(12)
    if xaiCondition == 3:
        # blank for now**************************************************
        # NOTE: every other will be empty because of the participant's turn**************************************************
        xaiTurn = []
    else:
        xaiTurn = []


    # 2. Preset halfway to compare:
    # Set to original halfway only if input is equal to starting state, this can update during the trial.
    halfwayState = [['C', 'C', 'C', '_', 'D', 'D', 'D'],  # 4
                    ['m', 'B', 'B', '_', 'j', 'k', 'l'],
                    ['m', 'A', 'A', '_', 'j', 'k', 'l'],
                    ['m', 'E', 'E', '_', 'F', 'F', 'l'],
                    ['G', 'G', 'G', 'i', '_', '_', '_'],
                    ['_', 'n', 'o', 'i', '_', '_', '_'],
                    ['_', 'n', 'o', 'i', 'H', 'H', '_']]
    
    
    # 3. Halfway state flag:
    # been to halfway state = 1
    # had not been to halfway state = 0
    beentoHalf = 0

    # 4. State solved flag:
    # unsolved = 0
    # solved = 1
    solvedFlag = 0

    # 5. Turn flag:
    # Participant = 0
    # Baxter = 1
    turnFlag = 1

    # 6. Turn counter:
    turnCounter = 0


    xaiCondition, halfwayState, beentoHalf, solvedFlag, turnFlag, turnCounter, xaiTurn = main(xaiCondition, halfwayState, beentoHalf, solvedFlag, turnFlag, turnCounter, xaiTurn)


