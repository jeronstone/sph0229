from PIL import Image, ImageDraw

h = 600
w = 600

dimx = 7
dimy = 7

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

    draw.rectangle(((xf-25,stepy*2-10),(xf,stepy*2+10)),fill=True)
    draw.rectangle(((xf-25,stepy*3-10),(xf,stepy*3+10)),fill=True)

    for i in range(len(state)):
        for j in range(len(state[0])):
            # TODO do rectangles as character dependent
            if not state[i][j] == '_':
                square = ((x0 + stepx*j, y0 + stepy*i),
                          (x0 + stepx*(j+1), y0 + stepy*(i+1)))
                draw.rectangle(square,fill="blue",outline='black')

    del draw
    
    image.show()


curState = [['I', 'I', '_', 'L', 'L','L', 'i'],
               ['J', 'J', '_', '_', 'b', '_', 'i'],
               ['k', '_', 'A', 'A', 'b', '_', 'h'],
               ['k', '_', '_', '_', 'b', '_', 'h'],
               ['k', '_', 'd', 'C', 'C', '_', 'g'],
               ['m', '_', 'd', '_', '_', '_', 'g'],
               ['m', '_', 'E', 'E', '_', 'F', 'F']]  #example

get_im_from_state(curState)