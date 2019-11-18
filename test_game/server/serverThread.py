import socket
import threading
import pickle
import random


class clientThread(threading.Thread):
    def __init__(self, client, getGameServerData, setGameServerData, sayGoodbye, playerID):
        size = 1024
        self.client = client
        self.headerLength = 10
        while True:
            try:
                # CHANGE client.py and here to update game server data and
                # local data
                # implemented rn is passing entire gameServerData dict
                msg = self.recieveHeader()
                if msg:
                    if msg == "get_game_data":
                        game = getGameServerData()
                        encodedMsg = pickle.dumps(game)
                        lenMsg = len(encodedMsg)
                        msg = f"{lenMsg:>{self.headerLength}}".encode() + \
                            encodedMsg
                        # print(msg)
                        client.send(msg)
                        continue
                    else:
                        #print(f'receive {msg}')
                        setGameServerData(msg)
                else:
                    print("Player disconnected")
                    sayGoodbye(playerID, playerID)
                    client.close()
                    break

            except socket.error as e:
                print(f"error: {e}")
                client.close()
                return False

    def _recieve_PickledMsg(self, msgLength):
        msgVal = self.client.recv(msgLength)
        return pickle.loads(msgVal)

    def recieveHeader(self):
        try:
            msgLength = (str(self.client.recv(10).decode()))
            if(msgLength):
                msgLength = int(msgLength)
                return self._recieve_PickledMsg(msgLength)
            return False
        except socket.error as e:
            print(e)
