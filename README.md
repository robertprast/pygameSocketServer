
# Pygame Server - Multi Threaded and Class Based

### Overview
Functional multiplayer setup for local and online multiplayer python games using sockets. Both server and client are implemented via classes. The server will spawn new threads for all new client connections and implements a semaphore for data synchronization when child threads are writing to its parent. The shared data is the game state and is protected when each child thread writes its new state and access the entire game state. 

### Communication Protocol 
The client has a seperate network class to handle all socket connections and recieving and sending data. The protocol is meant to ensure that the exact amount of bytes being read corresponds 1:1 with what is being sent. For example, a message that is 120 bytes long, but read on the client into a buffer of 2048 bytes is not a 1:1 correspondance. ll data being sent and received after connecting is sent with a custom protocol which corresponds with:

    Message Format:
      "HEADER+DATA"
      Header -> 10 characters for int value of pickled message length. Int value is right adjusted to a length of 10
      Data   -> Data is sent as a pickled message (serialized then encoded to bytes) and whose encoded length is denoted in the header

    Receiving Data:
        Data is recieved first by reading 10 bytes to get the header, the recieved value is decoded and stored as the data length var
        Then read X amount of bytes depending on the header and then depickle the message to the object that was orinally sent

    Sending Data:
        The data is first pickled and then the length of the pickled data is calculated. The information is then placed in it's repsective location in the message format
