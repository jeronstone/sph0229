# Some testing code
#

from PIL import Image, ImageDraw

h = 600
w = 600

dimx = 7
dimy = 7

image = Image.new(mode="L",size=(h,w),color=255)

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

draw.rectangle(((x0,stepy*4-10),(x0+25,stepy*4+10)),fill=True)
draw.rectangle(((x0,stepy*5-10),(x0+25,stepy*5+10)),fill=True)

del draw

image.save("grid_plus_gates.png")
#image.show()