import socket
import pickle
import pygame
from clientNetwork import *
import random


class clientGame:
    def __init__(self):
        # Pygame setup
        # Test commit
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.gameState = "running"
        self.playerColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Test Game")
        # Client network setup
        self._client = clientConnection()
        self.id = self._client.id

        # Call main game loop
        self.mainGameLoop()

    def drawGame(self, gameData):
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        for playerID, playerData in gameData["players"].items():
            xPos = gameData['players'][playerID]["position"][0]
            yPos = gameData['players'][playerID]['position'][1]

            pygame.draw.rect(self.screen, self.playerColor,
                             (xPos, yPos, 10, 10))
        pygame.display.update()

    def getGameData(self):
        self._client.sendMsg("get_game_data")
        return self._client.recieveHeader()

    # After connection we will then run our main game loop forever
    # Here we will continually ask the server for the newest game data, perform our own actions, send the actions back to the server so it can update the global game state
    # and then lastly draw all the changes
    def mainGameLoop(self):
        # Run forever!
        while self.gameState == "running":

            # Handle the user quiting the game via the X button
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState == "quit"
                    quit()

            # Get the full game data from the server, this calls the helper function in our clientNetwork file
            gameData = self.getGameData()

            # Set a local instance of the specific player from the global game data
            localPlayer = gameData["players"][self.id]

            # GAME LOGIC AREA -> First check if the game data exists though for safety
            # Perform player actions here
            if gameData != None:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_w]:
                    localPlayer['position'][1] -= 1
                if keys[pygame.K_a]:
                    localPlayer['position'][0] -= 1
                if keys[pygame.K_d]:
                    localPlayer['position'][0] += 1
                if keys[pygame.K_s]:
                    localPlayer['position'][1] += 1
            else:
                print("ERROR in gamedata")
                print(gameData)
                continue

            # Now update the instance of the global game data you recieved from the server with your new player
            # Draw the updates on your screen for your local player and all other players
            gameData["players"][self.id] = localPlayer
            self.drawGame(gameData)

            # Send player data back to server
            self._client.sendMsg(localPlayer)
            self.clock.tick(60)


game = clientGame()
