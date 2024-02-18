from PIL import Image, ImageDraw, ImageOps

# pixel dimension of image
h = 602
w = 602

# grid dimensions
dimx = 7
dimy = 7

# buffer for block offset from grid squares
buffer = 5

# gate height and width
gateh = 20
gatew = 15

# border size
borderw = 10

def get_im_from_state(state):
    image = Image.new(mode="RGB", size=(h,w), color="white")

    draw = ImageDraw.Draw(image)
    y0 = 0
    x0 = 0
    yf = image.height
    xf = image.width
    stepy = int(image.width/dimx)
    stepx = int(image.height/dimy)

    # draw grid
    for i in range(0, image.width, stepy):
        line = ((i, y0), (i, yf))
        draw.line(line, fill='black', width=3)

    for i in range(0, image.height, stepx):
        line = ((x0, i), (xf, i))
        draw.line(line, fill='black', width=3)

    # determine different blocks by character, add to dict
    state_dict = {}
    for i in range(len(state)):
        for j in range(len(state[0])):
            # if not state[i][j] == '_':
            #     square = ((x0 + stepx*j, y0 + stepy*i),
            #               (x0 + stepx*(j+1), y0 + stepy*(i+1)))
            #     draw.rectangle(square,fill="blue",outline='black')
            if not state[i][j] == '_':
                if not state[i][j] in state_dict.keys():
                    state_dict[state[i][j]] = [(i,j)]
                else:
                    state_dict[state[i][j]].append((i,j))

    # use dict to draw current blocks
    for k, v in state_dict.items():
        maxvx = max(v, key = lambda i : i[0])[0]
        maxvy = max(v, key = lambda i : i[1])[1]
        minvx = min(v, key = lambda i : i[0])[0]
        minvy = min(v, key = lambda i : i[1])[1]

        rect = ((x0 + (stepx*minvy) + buffer, y0 + (stepy*minvx) + buffer),
                (x0 + (stepx*(maxvy+1)) - buffer, y0 + (stepy*(maxvx+1)) - buffer))
        
        color='blue'
        if (k == 'A'):
            color='red'

        draw.rectangle(rect, fill=color, outline='black', width=2)

    # draw exit gates
    draw.rectangle(((xf - gatew, (stepy*2) - (gateh/2)), (xf, (stepy*2) + (gateh/2))), fill=True)
    draw.rectangle(((xf - gatew, (stepy*3) - (gateh/2)), (xf, (stepy*3) + (gateh/2))), fill=True)
    
    del draw

    # add border
    image = ImageOps.expand(image, border=borderw, fill='black')

    #print(state_dict)
    
    # save / show final image
    #image.show()
    image.save("test_state.png")


curState = [['I', 'I', '_', 'L', 'L','L', 'i'],
               ['J', 'J', '_', '_', 'b', '_', 'i'],
               ['k', '_', 'A', 'A', 'b', '_', 'h'],
               ['k', '_', '_', '_', 'b', '_', 'h'],
               ['k', '_', 'd', 'C', 'C', '_', 'g'],
               ['m', '_', 'd', '_', '_', '_', 'g'],
               ['m', '_', 'E', 'E', '_', 'F', 'F']]  #example

get_im_from_state(curState)