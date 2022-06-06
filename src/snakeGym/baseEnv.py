import socket
import subprocess
from datetime import datetime
from multiprocessing import Process, Queue
import os

import numpy as np

from .utils import plotLearning


class BaseEnv:
    def __init__(self) -> None:
        self.action_space = 4
        self.manualBattleSnakeCli = "BATTLESNAKE_CLI" in os.environ
        pass

    def plotLearning(self, x, scores, epsilons, filename, lines=None):
        plotLearning(x, scores, epsilons, filename, lines)

    def render(self):
        print("New Board State")
        boardToPrint = np.full(self.observation_space[0].shape, "░░", dtype=object)
        snakeIcons = ["⬜", "🟨", "🟥", "🟪", "🟩", "🟧", "🟫", "🟦"]

        for yLevel, y in enumerate(self.observation[0]):
            for xLevel, x in enumerate(y):
                if x != 0:
                    boardToPrint[yLevel][xLevel] = "🍎"

        for snakeNumber, state in enumerate(self.observation[1:]):
            for yLevel, y in enumerate(state):
                for xLevel, x in enumerate(y):
                    if x != 0:
                        boardToPrint[yLevel][xLevel] = snakeIcons[snakeNumber]

        for i in reversed(boardToPrint):
            for j in i:
                print(j, end="")
            print()

    def actionToStr(self, action):
        return ["up", "down", "left", "right"][action]

    def startBattleSnakeRunner(self, snakes, gamemode="standard"):

        self.startHttpServer()

        snakeUrls = ""
        for snakeName, snakeUrl in snakes.items():
            snakeUrls += f"--name {snakeName} --url {snakeUrl} "

        if not self.manualBattleSnakeCli:
            with open("cli.log", "a") as logfile:
                self.battleSnakeProc = subprocess.Popen(
                    f"battlesnake play {snakeUrls} -H {self.height} -W {self.width} -g {gamemode}".split(),
                    stdout=logfile,
                    stderr=logfile,
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
                client_connection.sendall("HTTP/1.0 200 OK\n\n{}".encode())
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

    def killBattleSnakeRunner(self):
        self.incomingQueue = Queue()
        self.incomingQueue.put(None)

        self.outgoingQueue = Queue()
        self.outgoingQueue.put(None)

        if not self.manualBattleSnakeCli:
            if self.battleSnakeProc:
                self.battleSnakeProc.kill()

        if self.server_socket:
            self.server_socket.close()
            self.reader_p.terminate()
            self.reader_p.join()

        # print(self.incomingQueue.qsize(), self.outgoingQueue.qsize())

        while True:
            if self.incomingQueue.get() == None:
                break

        while True:
            if self.outgoingQueue.get() == None:
                break
