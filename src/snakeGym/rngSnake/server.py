import os

from flask import Flask, request

import logic

app = Flask(__name__)


@app.get("/")
def handle_info():
    return logic.get_info()


@app.post("/start")
def handle_start():
    return "ok"


@app.post("/move")
def handle_move():
    move = logic.choose_move(request.get_json())
    return {"move": move}


@app.post("/end")
def handle_end():
    return "ok"


if __name__ == "__main__":
    host = "localhost"
    port = int(os.environ.get("PORT", "8080"))

    app.env = "development"
    app.run(host=host, port=port, debug=False)
