import base64
import io
from time import sleep

from flask import Flask
from flask import make_response
from flask import send_file

app = Flask(__name__)


@app.route("/")
def entry():
    return '<a href="/display_pixel/0">A page with a pixel'


@app.route("/display_pixel/<int:id>")
def display_pixel(id):
    # sleep(1)
    if id > 5:
        return '<a href="/display_pixel/count">counter</a>'
    else:
        return f'<img src="/pixel"/><a href="/display_pixel/{ id + 1}">next pixel</a>'


@app.route("/pixel")
def pixel():
    pixel.counter += 1

    # This is a 1x1 pixel transparent PNG image, base64-encoded
    img_data = b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg=="
    img_bytes = base64.b64decode(img_data)

    img_io = io.BytesIO()
    img_io.write(img_bytes)
    img_io.seek(0)

    response = make_response(send_file(img_io, mimetype="image/png"))
    # Cache for 1 year
    response.headers["Cache-Control"] = "public, max-age=31536000"
    return response


pixel.counter = 0


@app.route("/display_pixel/count")
def display_pixel_count():
    return f"count:{pixel.counter}"
