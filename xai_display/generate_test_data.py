from PIL import Image, ImageDraw, ImageFont

policies = ["good","okay","bad"]

for i in range(1, 100):
    for j in policies:
        img = Image.new('RGB',(500,500),(255,255,255))
        d = ImageDraw.Draw(img)
        fnt = ImageFont.truetype("arial.ttf", 50)
        d.text((150,150), "Turn {x}, {pol}".format(x=i,pol=j),fill=(0,0,0), font=fnt)
        img.save("{x}_{pol}.jpeg".format(x=i,pol=j[0]))

        with open("{x}_{pol}.txt".format(x=i,pol=j[0]), 'w') as f:
            f.write("Turn {x}, {pol} explanation".format(x=i,pol=j))
        f.close()