from PIL import Image, ImageDraw

h = 600
w = 600

dimx = 7
dimy = 7

buffer = 5

def get_im_from_state(state):
    image = Image.new(mode="RGB",size=(h,w),color="white")

    draw = ImageDraw.Draw(image)
    y0 = 0
    x0 = 0
    yf = image.height
    xf = image.width
    stepy = int(image.width/dimx)
    stepx = int(image.height/dimy)

    for i in range(0, image.width, stepy):
        line = ((i, y0), (i, yf))
        draw.line(line, fill=128)

    for i in range(0, image.height, stepx):
        line = ((x0, i), (xf, i))
        draw.line(line, fill=128)

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

    for k, v in state_dict.items():
        maxvx = max(v, key = lambda i : i[0])[0]
        maxvy = max(v, key = lambda i : i[1])[1]
        minvx = min(v, key = lambda i : i[0])[0]
        minvy = min(v, key = lambda i : i[1])[1]

        rect = ((x0+stepx*minvy+buffer,y0+stepy*minvx+buffer),(x0+stepx*(maxvy+1)-buffer,y0+stepy*(maxvx+1)-buffer))
        draw.rectangle(rect,fill="blue",outline='black',width=2)

    draw.rectangle(((xf-25,stepy*2-10),(xf,stepy*2+10)),fill=True)
    draw.rectangle(((xf-25,stepy*3-10),(xf,stepy*3+10)),fill=True)

    del draw

    print(state_dict)
    
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