import socket
import pickle
import pygame
from clientNetwork import *
import random


class clientGame:
    def __init__(self):
        # Pygame setup
        pygame.init()
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.gameState = "running"
        self.playerColor = (random.randint(0, 255), random.randint(
            0, 255), random.randint(0, 255))
        self.clock = pygame.time.Clock()
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

    def mainGameLoop(self):
        while self.gameState == "running":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.gameState == "quit"
                    quit()

            # Get the full game data
            gameData = self.getGameData()
            # Perform player actions here
            if gameData != None:
                gameData["players"][self.id]["position"][1] += random.randint(
                    -1, 1)
                gameData["players"][self.id]["position"][0] += random.randint(
                    -1, 1)
            else:
                print("ERROR in gamedata")
                print(gameData)
            # Draw game
            self.drawGame(gameData)

            # Send player data back to server
            self._client.sendMsg(gameData["players"][self.id])
            self.clock.tick(60)


game = clientGame()
