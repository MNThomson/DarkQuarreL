import os
from typing import Any, Dict

import uvicorn
from fastapi import FastAPI

import logic

app = FastAPI()


@app.get("/")
def handle_info():
    return logic.get_info()


@app.post("/start")
def handle_start(req: Dict[Any, Any]):
    return "ok"


@app.post("/move")
def handle_move(req: Dict[Any, Any]):
    move = logic.choose_move(req)
    return {"move": move}


@app.post("/end")
def handle_end(req: Dict[Any, Any]):
    return "ok"


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=int(os.environ.get("PORT", "8080")))

# uvicorn test:app --reload
