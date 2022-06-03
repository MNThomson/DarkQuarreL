import json
import socket
import subprocess
from datetime import datetime
from multiprocessing import Process, Queue

import numpy as np

from convert import convertJsonToMatrix

from .baseEnv import BaseEnv


def actionToStr(action):
    return ["up", "down", "right", "left"][action]


class BattlegroundsDuel(BaseEnv):
    def __init__(self) -> None:
        self.observation_space = np.zeros((9, 11, 11), dtype=np.int8)
        self.action_space = 4
        self.observation = None
        self.proc = None
        self.server_socket = None
        self.incomingQueue = Queue()
        self.outgoingQueue = Queue()

    def reset(self):
        if self.proc:
            self.proc.kill()

        if self.server_socket:
            self.server_socket.close()
            self.reader_p.terminate()
            self.reader_p.join()

        self.startBattleSnake()

        self.observation = convertJsonToMatrix(self.incomingQueue.get())
        return self.observation

    def step(self, action):
        action = actionToStr(action)
        self.outgoingQueue.put(action)

        reward = 0
        done = False

        if not self.isEnd():
            data = self.incomingQueue.get()
            if data == "END":
                data = json.loads(self.incomingQueue.get())
                if len(data["board"]["snakes"]) == 0:
                    iWon = False
                else:
                    iWon = data["board"]["snakes"][0]["name"] == "Snake1"
                done = True
                reward = 1 if iWon else -1

            else:
                self.observation = convertJsonToMatrix(data)

        return self.observation, reward, done, None

    def isEnd(self):
        return self.proc.poll() is None

    def startBattleSnake(self):
        self.startHttpServer()

        self.proc = subprocess.Popen(
            f"battlesnake play --name Snake1 --url http://localhost:8080 --name Snake2 --url http://localhost:8000 -W 11 -H 11 -o game/{datetime.now().time()}.json".split(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=False,
        )

    def startHttpServer(self):
        SERVER_HOST = "127.0.0.1"
        SERVER_PORT = 8080

        # Create socket
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((SERVER_HOST, SERVER_PORT))
        self.server_socket.listen(1)
        # print("Listening on port %s ..." % SERVER_PORT)

        self.reader_p = Process(
            target=self.handleHttpServer,
            args=(
                (self.incomingQueue),
                (self.outgoingQueue),
            ),
        )
        self.reader_p.daemon = True
        self.reader_p.start()

    def handleHttpServer(self, incomingQueue, outgoingQueue):
        while True:
            # Wait for client connections
            client_connection, client_address = self.server_socket.accept()

            # Get the client request
            request = client_connection.recv(2048).decode()
            data = request.splitlines()[-1].encode().decode()

            if "move" not in request:
                client_connection.sendall("HTTP/1.0 200 OK\n".encode())
                client_connection.close()
                if "end" in request:
                    incomingQueue.put("END")
                    incomingQueue.put(data)
                continue

            incomingQueue.put(data)
            move = outgoingQueue.get()

            # Return an HTTP response
            response = "HTTP/1.0 200 OK\n\n" + '{"move":"' + move + '"}'

            client_connection.sendall(response.encode())

            # Close connection
            client_connection.close()
