import pygame  
import sys  
import random
import time
#Sprite class   

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MAX_FOOD = 1
PLAYER_SPAWN = [2, 0]
MAP_LOOP = False
bg = [0, 0, 0]  


class GameState:
    def __init__(self, gridSize, screenSize, fps, maxFood):
        
        pygame.init()  
        self.clock = pygame.time.Clock()
        self.screenSize = screenSize
        self.blockSize = self.screenSize[0] // gridSize
        self.fps = fps
        self.maxFood = maxFood


        self.screen = pygame.display.set_mode(self.screenSize)  
        self.grid = [[0 for x in range(gridSize)] for y in range(gridSize)]
        self.PlayerSize = 1
        self.movementDirection = [0, 1]
        self.PlayerBody = [PLAYER_SPAWN]
        self.PlayerHead = PLAYER_SPAWN
        self.FoodSpawned = 0
        self.GameOver = 0
        self.playerMoves = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
    

    def printGrid(self):
        print("\n"*200)
        for i in self.grid:
            for j in i:
                print(j, end=" ")
            print()

    def movePlayerBody(self):
        for i in range(0, len(self.PlayerBody)):
            self.grid[self.PlayerBody[i][0]][self.PlayerBody[i][1]] = 0

        if len(self.PlayerBody) < self.PlayerSize:
            # self.PlayerBody.append([self.PlayerHead[0], self.PlayerHead[1]])
            self.PlayerBody.insert(0, [self.PlayerHead[0], self.PlayerHead[1]])
        else:
            self.PlayerBody.pop()
            self.PlayerBody.insert(0, [self.PlayerHead[0], self.PlayerHead[1]])


        for part in self.PlayerBody:
            self.grid[part[0]][part[1]] = 1
        self.grid[self.PlayerHead[0]][self.PlayerHead[1]] = 3


    def checkBoundary(self):
        if MAP_LOOP:
            if self.PlayerHead[0] > len(self.grid) - 1:
                self.PlayerHead[0] = 0
                self.PlayerBody[0] = [0, self.PlayerHead[1]]
            if self.PlayerHead[0] < 0:
                self.PlayerHead[0] = len(self.grid) - 1
                self.PlayerBody[0] = [len(self.grid) - 1, self.PlayerHead[1]]
            if self.PlayerHead[1] > len(self.grid) - 1:
                self.PlayerHead[1] = 0
                self.PlayerBody[0] = [self.PlayerHead[0], 0]
            if self.PlayerHead[1] < 0:
                self.PlayerHead[1] = len(self.grid) - 1
                self.PlayerBody[0] = [self.PlayerHead[0], len(self.grid) - 1]
        else:
            if self.PlayerHead[0] > len(self.grid) - 1:
                return True
            if self.PlayerHead[0] < 0:
                return True
            if self.PlayerHead[1] > len(self.grid) - 1:
                return True
            if self.PlayerHead[1] < 0:
                return True
        return False


    def checkCollision(self):
        for i in range(1, len(self.PlayerBody)):
            if self.PlayerHead == self.PlayerBody[i]:
                return True
        return False
        

    def getGridPosColor(self, pos):
        if self.grid[pos[0]][pos[1]] == 0:
            # Empty
            return WHITE
        if self.grid[pos[0]][pos[1]] == 1:
            # Player Body
            return GREEN
        if self.grid[pos[0]][pos[1]] == 2:
            # Food
            return RED
        if self.grid[pos[0]][pos[1]] == 3:
            # Player Head
            return BLACK


    def movePlayer(self, key):
        if key[self.playerMoves[0]] or key[self.playerMoves[1]] or key[self.playerMoves[2]] or key[self.playerMoves[3]]:
            if key[self.playerMoves[0]]:
                self.PlayerHead[0] -= 1
                self.movementDirection = [-1, 0]
            elif key[self.playerMoves[1]]:
                self.PlayerHead[0] += 1
                self.movementDirection = [1, 0]
            elif key[self.playerMoves[2]]:
                self.PlayerHead[1] -= 1
                self.movementDirection = [0, -1]
            elif key[self.playerMoves[3]]:
                self.PlayerHead[1] += 1
                self.movementDirection = [0, 1]
        else:
            self.PlayerHead[0] += self.movementDirection[0]
            self.PlayerHead[1] += self.movementDirection[1]

    def checkFoodEaten(self):
        if self.grid[self.PlayerHead[0]][self.PlayerHead[1]] == 2:
            self.FoodSpawned -= 1
            self.PlayerSize += 1
            self.grid[self.PlayerHead[0]][self.PlayerHead[1]] = 3

    def drawGrid(self):
        for x in range(0, self.screenSize[0], self.blockSize):
            for y in range(0, self.screenSize[1], self.blockSize):
                rect = pygame.Rect(x, y, self.blockSize, self.blockSize)
                
                pygame.draw.rect(self.screen,  self.getGridPosColor((x//self.blockSize,y//self.blockSize)), rect, 0)
                pygame.draw.rect(self.screen, BLACK, rect, 1)


    def spawnFood(self):
        if self.FoodSpawned < self.maxFood:
            while self.FoodSpawned < self.maxFood:
                random_x = round(random.randint(0, len(self.grid) - 1))
                random_y = round(random.randint(0, len(self.grid) - 1))

                if self.grid[random_x][random_y] != 0:
                    continue

                self.grid[random_x][random_y] = 2
                self.FoodSpawned += 1
    
    def runGame(self):  
    
  
        while True:  
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:  
                    return False  
            
            # Movement
            key = pygame.key.get_pressed()  
            self.movePlayer(key)

            if self.checkBoundary():
                print("Game Over")
                break

            self.spawnFood()
            self.checkFoodEaten()

            

            self.movePlayerBody()

            # ! Draw
            self.screen.fill(bg)  
            self.drawGrid()
            
            # Check for self collisions
            if self.checkCollision():
                print("Game Over")
                break

            pygame.display.update()  
            self.clock.tick(self.fps)  

        # ! Game Over
        font = pygame.font.SysFont('arial', 40)
        gameOver = font.render("Game Over", True, RED)
        self.screen.blit(gameOver, (self.screenSize[0]/2 - gameOver.get_width()/2, self.screenSize[1]/2 - gameOver.get_height()/2))
        pygame.display.update()
        self.GameOver = 1

        # Close the window and quit.
        pygame.quit()  
    


# gameState = GameState(gridSize)



# Define keys for player movement  





