import socket
import pickle
import pygame

# Simple socket network connection for the client
# Here we handle first connecting to the main server , parsing the unique ID we get back
# Then we have helper functions for recieving a message and sending a message. The helper functions conform the below protocol

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


class clientConnection:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host = '127.0.0.1'
        port = 9999
        self.headerLength = 10
        self.socket.connect((host, port))
        self.id = self.socket.recv(256).decode()
        print(f"Connected to {host} with id of {self.id}")

    def _recieve_PickledMsg(self, msgLength):
        try:
            # print(msgLength)
            msgVal = self.socket.recv(msgLength)
            # print(msgVal)
            return pickle.loads(msgVal)
        except socket.error as e:
            print("error in recv_PickledMsg")
            print(e)

    def recieveHeader(self):
        try:
            msgLength = (str(self.socket.recv(10).decode()))
            if(msgLength):
                msgLength = int(msgLength)
                msg = self._recieve_PickledMsg(msgLength)
                return msg
            else:
                print("error in msg_recv")
        except socket.error as e:
            print("error in recieveHeader")
            print(e)

    def sendMsg(self, msg):
        encodedMsg = pickle.dumps(msg)
        lenMsg = len(encodedMsg)
        msg = f"{lenMsg:>{self.headerLength}}".encode()+encodedMsg
        self.socket.send(msg)
