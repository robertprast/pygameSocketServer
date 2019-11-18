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
        # print("SETTING GAME DATA TO")
        # print(data)
        # print(self.gameServerData)
        gameServerSemaphore.release()
        return True

    def getGameServerData(self):
        gameServerSemaphore.acquire()
        localCopy = self.gameServerData
        gameServerSemaphore.release()
        # print("WEI")
        # print(localCopy)
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
                # msg = f'ID:{random.randint(12345,123456)}' +
                # msg = f"{len(pickle.dumps(msg)):>{self.headerLength}}".encode(
                # ) + pickle.dumps(msg)
                # print(msg)
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


# # create a socket object
# serversocket = socket.socket(
#     socket.AF_INET, socket.SOCK_STREAM)
# serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# host = '127.0.0.1'
# port = 9999
# serversocket.bind((host, port))
# serversocket.listen(5)
# headLength = 10
# connected_clients = []


# def listenToClient(client, addr):
#     size = 1024
#     while True:
#         try:
#             data = client.recv(size)
#             if data:
#                 # Set the response to echo back the recieved data
#                 msg = data
#                 # stringToSend=f"RANDOM NONCE: {random.randint(0,1000)}"
#                 # print(stringToSend)
#                 msg = (
#                     msg+pickle.dumps(f"RANDOM Nonce: {random.randint(0,5555555)}"))
#                 lenMsg = len(msg)
#                 msg = (pickle.loads(msg))
#                 print(msg)
#                 msg = f"{lenMsg:>{headLength}}".encode()+pickle.dumps(msg)
#                 # print(msg)
#                 client.send(msg)

#             else:
#                 raise error('Client disconnected')
#         except:
#             client.close()
#             return False


# while True:
#     # establish a connection
#     clientsocket, addr = serversocket.accept()

#     print("Got a connection from %s" % str(addr))

#     connected_clients.append(clientsocket)

#     msg = 'Thank you for connecting' + "\r\n"

#     msg = f"{len(pickle.dumps(msg)):>{headLength}}".encode()+pickle.dumps(msg)
#     # print(msg)
#     clientsocket.send(msg)

#     try:
#         threading.Thread(target=listenToClient,
#                          args=(clientsocket, addr,)).start()
#     except:
#         print("error")
