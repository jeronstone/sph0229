import webbrowser
import os

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

def get_html(turn):
    f = open(turns[turn]["text"],"r")
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
        image=turns[turn]["image"],
        text=file_text
    )

for i in range(1,2):
    f = open("index.html","w")
    f.write(get_html(i))
    f.close()

    webbrowser.open(os.getcwd() + "/index.html")