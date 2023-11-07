import webbrowser
import os

tree_lut = [1,2,3]

'''
turns = {
    1: {
        "image": "local_im_1.jpeg",
        "text": "local_txt_1.txt"
    },
    2: {
        "image": "local_im_2.jpeg",
        "text": "local_txt_2.txt"
    },

}
'''

def get_turn_image(turn):
    return "local_im_{turn_num}.jpeg".format(turn_num=turn)

def get_turn_exp_fi(turn):
    return "local_txt_{turn_num}.txt".format(turn_num=turn)

def get_html(turn):
    f = open(get_turn_exp_fi(turn),"r")
    file_text = f.read()
    f.close()
    return '''
    <!doctype html>
    <html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Demo</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
    </head>
    <body>
        <div class="container p-5 my-5 bg-primary text-white">
            <img src="{image}" class="img-fluid rounded mx-auto d-block">
        </div>
        <div class="container p-5 my-5 bg-primary text-white">
            <p class="lead text-center">{text}</h1>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
    </body>
    </html>
    '''.format(
        image=get_turn_image(turn),
        text=file_text
    )

def refresh(turn):
    f = open("index.html","w")
    f.write(get_html(turn))
    f.close()
    webbrowser.open(os.getcwd() + "/index.html")

level=0
current=1
refresh(current)

while(1):
    input = input()
    level+=1
    if input == "l":
        current = 2**level + current - 1
    elif input == "r":
        current = 2**level + current
    else:
        exit(1)
    refresh(current)

'''
    <div class="container p-5 my-5 bg-primary text-white">
        <script>
            function goLeft() {
            }
            function goRight() {
            }
        </script>
        <button onclick="goLeft()" class="btn btn-success">Left Tree</a>
        <button onclick="goRight()" class="btn btn-danger">Right Tree</button>
    </div>
'''