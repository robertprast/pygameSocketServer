import socket
import threading
from serverThread import *

gameServerSemaphore = threading.Semaphore()


class server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clientList = []
        self.headerLength = 10
        self.gameServerData = {"players": {}, "games": {}}
        self.gamesCount = 0
        self.playerCount = 0
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))
        self.serversocket.listen(5)
        self.listenForClints()

    def setGameServerData(self, data):
        gameServerSemaphore.acquire()
        self.gameServerData['players'][data['id']] = data
        gameServerSemaphore.release()
        return True

    def getGameServerData(self):
        gameServerSemaphore.acquire()
        localCopy = self.gameServerData
        gameServerSemaphore.release()
        return localCopy

    def sayGoodbye(self, player_id, game_id):
        print(f"goodbye from player {player_id}")
        gameServerSemaphore.acquire()
        self.gameServerData["players"].pop(str((player_id)))
        if self.gameServerData["players"] == {}:
            print("NO ACTIVE GAMES ")
            # self.gameServerData["games"].pop(game_id)
        print(self.gameServerData)
        gameServerSemaphore.release()

    def listenForClints(self):
        while True:
            try:
                # establish a connection
                clientsocket, addr = self.serversocket.accept()
                print("Got a connection from %s" % str(addr))

                gameServerSemaphore.acquire()
                self.gameServerData["players"][str(self.playerCount)] = {
                    'id': str(self.playerCount), "position": [400, 400]}
                gameServerSemaphore.release()
                print(self.gameServerData["players"][str(self.playerCount)])
                clientsocket.send(
                    self.gameServerData["players"][str(self.playerCount)]['id'].encode())

                threading.Thread(target=clientThread,
                                 args=(clientsocket, self.getGameServerData, self.setGameServerData, self.sayGoodbye, self.playerCount, )).start()
                self.playerCount += 1
            except socket.error as e:
                print("error making client thread")
                print(e)


host = '127.0.0.1'
port = 9999
server1 = server(host, port)


