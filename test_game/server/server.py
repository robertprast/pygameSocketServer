import socket
import threading
from serverThread import clientThread

gameServerSemaphore = threading.Semaphore()


class server:
    def __init__(self, host, port):
        # Game server variables
         # GAME LOGIC AREA
        self.gameServerData = {"players": {}, "games": {}}
        self.playerCount = 0

        # Connection variables
        self.host = host
        self.port = port

        # Init the socket
        self.serversocket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.host, self.port))

        # Listen for connections, with a Queue of 5
        # Then call the main listen loop
        self.serversocket.listen(5)
        self.listenForClints()

    # Set the game data
    def setGameServerData(self, data):
        gameServerSemaphore.acquire()
        self.gameServerData['players'][data['id']] = data
        gameServerSemaphore.release()
        return True

    # Get the game data
    def getGameServerData(self):
        gameServerSemaphore.acquire()
        localCopy = self.gameServerData
        gameServerSemaphore.release()
        return localCopy

    # Function to log a player disconnecting
    # This will remove them from the game data as well
    def sayGoodbye(self, player_id, game_id):
        print(f"goodbye from player {player_id}")
        gameServerSemaphore.acquire()
        self.gameServerData["players"].pop(str((player_id)))
        if self.gameServerData["players"] == {}:
            print("NO ACTIVE GAMES ")
            # self.gameServerData["games"].pop(game_id)
        print(self.gameServerData)
        gameServerSemaphore.release()

    # This is where we will run forever listening for clients to connect
    # Once they connect we update our game variables, send them their ID, and then spawn a new thread for them
    def listenForClints(self):
        while True:
            try:
                # establish a connection
                clientsocket, addr = self.serversocket.accept()
                print("Got a connection from %s" % str(addr))

                # Add the player to the game data
                gameServerSemaphore.acquire()
                self.gameServerData["players"][str(self.playerCount)] = {
                    'id': str(self.playerCount), "position": [400, 400]}
                gameServerSemaphore.release()
                print(self.gameServerData["players"][str(self.playerCount)])

                # Send the players ID back to the client
                clientsocket.send(
                    self.gameServerData["players"][str(self.playerCount)]['id'].encode())

                # Start a new thread for this specific client
                threading.Thread(target=clientThread,
                                 args=(clientsocket, self.getGameServerData, self.setGameServerData, self.sayGoodbye, self.playerCount, )).start()

                # Increase the player count
                self.playerCount += 1

            # Handle any errors that came in during the connection
            except socket.error as e:
                print("error making client thread")
                print(e)


# Setting our IP and Port to listen on
host = '127.0.0.1'
port = 9999

# Starting the server!
server1 = server(host, port)
