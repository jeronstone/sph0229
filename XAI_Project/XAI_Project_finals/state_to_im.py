from PIL import Image, ImageDraw, ImageOps
import cv2
import numpy as np

# color def
_BLUE = (68, 115, 197)
_LGR = (226, 240, 217)
_DGR = (114, 172, 69)
_ARRGR = (167, 210, 139)
_RED = (251, 1, 2)

# pixel dimension of image
h = 602
w = 602

# grid dimensions
dimx = 7
dimy = 7

# buffer for block offset from grid squares
buffer_default = 7
prev_border_buffer = 20

# gate height and width
gateh = 20
gatew = 15

# arrow defs
arrow_line_width = 15
arrow_triangle_size = 35

# border size
borderw = 10

def get_im_from_state(state, prev):
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
    diff = ''
    state_dict = {}
    for i in range(len(state)):
        for j in range(len(state[0])):
            if not state[i][j] == '_':
                if not state[i][j] in state_dict.keys():
                    state_dict[state[i][j]] = [(i,j)]
                else:
                    state_dict[state[i][j]].append((i,j))      
            elif not state[i][j] == prev[i][j]:
                diff = prev[i][j]
    
    for i in range(len(prev)):
        for j in range(len(prev)):
            if prev[i][j] == diff:
                if not 'prev' in state_dict.keys():
                    state_dict['prev'] = [(i,j)]
                else:
                    state_dict['prev'].append((i,j))

    if diff == '':
        print("ruh roh diff")

    def get_rect(k, v, *args, **kwargs):
        buffer = kwargs.get('buffer', buffer_default)
        maxvx = max(v, key = lambda i : i[0])[0]
        maxvy = max(v, key = lambda i : i[1])[1]
        minvx = min(v, key = lambda i : i[0])[0]
        minvy = min(v, key = lambda i : i[1])[1]

        return ((x0 + (stepx*minvy) + buffer, y0 + (stepy*minvx) + buffer),
                (x0 + (stepx*(maxvy+1)) - buffer, y0 + (stepy*(maxvx+1)) - buffer))

    # use dict to draw blocks (skip diffs)
    for k, v in state_dict.items():
        rect = get_rect(k, v)
        
        color=_BLUE
        if (k == 'A'):
            color=_RED
        elif (k == diff or k == 'prev'):
            continue

        draw.rectangle(rect, fill=color, outline='black', width=2)

    # get current and previous block info
    prev_rect = get_rect('prev', state_dict['prev'])
    prev_rect_inner = get_rect('prev',state_dict['prev'],buffer=prev_border_buffer)
    curr_rect = get_rect(diff, state_dict[diff])

    '''
        the following code is very messy and unreadable and it has some magic numbers :(
        to get the gist, just know:
        
            <prev/curr>_rect[0][0] -> x0 (top left x)
            <prev/curr>_rect[0][1] -> y0 (top left y)
            <prev/curr>_rect[1][0] -> x1 (bottom right x)
            <prev/curr>_rect[1][1] -> x1 (bottom right y)
        
        visual:
        
        (rect[0][0], rect[0][1])    * ----------------------
                                    |                       |
                                    |                       |
                                     ---------------------- * (rect[1][0], rect[1][1])
    '''

    # get directional information and create base and point for arrow
    arrow_line_info = None
    arrow_triangle_info = None
    if prev_rect[0][0] > curr_rect[0][0]:
        #left
        base = (prev_rect[1][0]-40,((prev_rect[0][1]+prev_rect[1][1])//2))
        point = (curr_rect[0][0]+60, base[1])
        arrow_line_info = (base, point)
        arrow_triangle_info = [(point[0],point[1]+arrow_triangle_size),(point[0],point[1]-arrow_triangle_size),(point[0]-arrow_triangle_size,point[1])]

    elif prev_rect[0][1] < curr_rect[0][1]:
        #down
        base = (((prev_rect[0][0]+prev_rect[1][0])//2), prev_rect[0][1]+40)
        point = (base[0], curr_rect[1][1]-60)
        arrow_line_info = (base, point)
        arrow_triangle_info = [(point[0]+arrow_triangle_size,point[1]),(point[0]-arrow_triangle_size,point[1]),(point[0], point[1]+arrow_triangle_size)]

    elif prev_rect[0][0] < curr_rect[0][0]:
        #right
        base = (prev_rect[0][0]+40,((prev_rect[0][1]+prev_rect[1][1])//2))
        point = (curr_rect[1][0]-60, base[1])
        arrow_line_info = (base, point)
        arrow_triangle_info = [(point[0],point[1]+arrow_triangle_size),(point[0],point[1]-arrow_triangle_size),(point[0]+arrow_triangle_size,point[1])]

    elif prev_rect[0][1] > curr_rect[0][1]:
        #up
        base = (((prev_rect[0][0]+prev_rect[1][0])//2), prev_rect[1][1]-40)
        point = (base[0], curr_rect[0][1]+60)
        arrow_line_info = (base, point)
        arrow_triangle_info = [(point[0]+arrow_triangle_size,point[1]),(point[0]-arrow_triangle_size,point[1]),(point[0], point[1]-arrow_triangle_size)]

    if not arrow_line_info or not arrow_triangle_info:
        print('ruh ruh direction')

    # draw previous and current
    draw.rectangle(prev_rect, fill=_ARRGR, outline='black', width=2)
    draw.rectangle(prev_rect_inner, fill=_LGR, width=2)
    draw.rectangle(curr_rect, fill=_DGR, outline='black', width=2)

    # draw exit gates
    draw.rectangle(((xf - gatew, (stepy*2) - (gateh/2)), (xf, (stepy*2) + (gateh/2))), fill=True)
    draw.rectangle(((xf - gatew, (stepy*3) - (gateh/2)), (xf, (stepy*3) + (gateh/2))), fill=True)
    
    # draw arrow
    draw.line(arrow_line_info, width=arrow_line_width, fill=_ARRGR)
    draw.polygon(arrow_triangle_info, fill=_ARRGR)

    del draw

    # add border
    image = ImageOps.expand(image, border=borderw, fill='black')

    # draw arrow (old)
    # npa = np.array(image)
    # npa = cv2.arrowedLine(npa, arrow_info[0], arrow_info[1], _ARRGR, 12, tipLength=.2)
    # image = Image.fromarray(npa)
    
    # rotate 180 deg
    image = image.rotate(180)
    
    # save / show final image
    #image.show()
    image.save("xai_exp.png")
    return "xai_exp.png"

currState =    [['I', 'I', '_', 'L', 'L','L', 'i'],
               ['J', 'J', '_', '_', 'b', '_', 'i'],
               ['k', '_', 'A', 'A', 'b', 'h', '_'],
               ['k', '_', '_', '_', 'b', 'h', '_'],
               ['k', '_', 'd', 'C', 'C', '_', 'g'],
               ['m', '_', 'd', '_', '_', '_', 'g'],
               ['m', '_', 'E', 'E', '_', 'F', 'F']]  #example


prevState =   [['I', 'I', '_', 'L', 'L','L', 'i'],
               ['J', 'J', '_', '_', 'b', '_', 'i'],
               ['k', '_', 'A', 'A', 'b', '_', '_'],
               ['k', '_', '_', '_', 'b', '_', '_'],
               ['k', '_', 'd', 'C', 'C', 'h', 'g'],
               ['m', '_', 'd', '_', '_', 'h', 'g'],
               ['m', '_', 'E', 'E', '_', 'F', 'F']]  #example

get_im_from_state(currState, prevState)