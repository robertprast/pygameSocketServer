import socket
import threading
import pickle
import random

# Each time a client connects, they will spawn a new thread whose main code is an instance of this class
# We pass refrences to the main functions of getting the game data, setting the game data, and handling a disconnect
# These functions are in the main server parent thread and their data is protected by a sempaphore so multple clients can safely access data
# We also send the playerID so the thread knows exactly who it is

'''
Message Format:
  "HEADER+DATA"
  Header -> 10 characters for int value of pickled message length. Int value is right adjusted to a length of 10
  Data   -> Data is sent as a pickled message (serialized then encoded to bytes) and whose encoded length is denoted in the header

Receiving Data:
    Data is recieved first by reading 10 bytes to get the header, the recieved value is decoded and stored as the data length var
    Then read X amount of bytes depending on the header and then depickle the message to the object that was orinally sent

Sending Data:
    The data is first pickled and then the length of the pickled data is calculated. The information is then placed in it's repsective location in the message format
'''


class clientThread(threading.Thread):
    def __init__(self, client, getGameServerData, setGameServerData, sayGoodbye, playerID):
        # Set its class variables to the instance of the socket connection
        self.client = client
        # Communication protocl defined headerLength
        self.headerLength = 10

        # Run forever loop, listening for commands and sending the game data back to the client
        while True:
            try:
                # Wait for the client to send a command, and then process it. The client always speaks first
                msg = self._recieveHeader()
                if msg:
                    # Send the game data based on the get_game_data command
                    if msg == "get_game_data":
                        game = getGameServerData()
                        encodedMsg = pickle.dumps(game)
                        lenMsg = len(encodedMsg)
                        msg = f"{lenMsg:>{self.headerLength}}".encode() + \
                            encodedMsg
                        # print(msg)
                        client.send(msg)
                        continue
                    # Other command is updating the game server data for this specific client
                    else:
                        #print(f'receive {msg}')
                        setGameServerData(msg)

                # Handle the socket dropping and the user disconnecting here
                else:
                    print("Player disconnected")
                    sayGoodbye(playerID, playerID)
                    client.close()
                    break

            except socket.error as e:
                print(f"error: {e}")
                client.close()

    '''
    Helper functions to format data correctly
    '''

    def _recieve_PickledMsg(self, msgLength):
        msgVal = self.client.recv(msgLength)
        return pickle.loads(msgVal)

    def _recieveHeader(self):
        try:
            msgLength = (str(self.client.recv(10).decode()))
            if(msgLength):
                msgLength = int(msgLength)
                return self._recieve_PickledMsg(msgLength)
            return False
        except socket.error as e:
            print(e)
