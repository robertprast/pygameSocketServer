import socket
import pickle
import pygame

# Simple socket network connection
'''
Communication protocol:
    Connect to server -> server responds with id value as string
    All other messages are sent and recved encoded:
        Msg format -> Len of msg (10 chars)+Pickled_Msg 
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
