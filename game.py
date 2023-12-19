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
class GameState:
    def __init__(self, gridSize):
        self.grid = [[0 for x in range(gridSize)] for y in range(gridSize)]
        self.PlayerSize = 1
        self.movementDirection = [0, 1]
        self.PlayerBody = [PLAYER_SPAWN]
        self.PlayerHead = PLAYER_SPAWN
        self.grid[PLAYER_SPAWN[0]][PLAYER_SPAWN[1]] = 1
        self.FoodSpawned = 0

pygame.init()  
clock = pygame.time.Clock()  
fps = 3
bg = [0, 0, 0]  
screenSize =[600, 600]  
screen = pygame.display.set_mode(screenSize)  

blockSize = 50
gridSize = int(screenSize[0] // blockSize)
gameState = GameState(gridSize)



# Define keys for player movement  
playerMoves = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  

def printGrid():
    print("\n"*200)
    for i in gameState.grid:
        for j in i:
            print(j, end=" ")
        print()

def movePlayerBody():
    for i in range(0, len(gameState.PlayerBody)):
        gameState.grid[gameState.PlayerBody[i][0]][gameState.PlayerBody[i][1]] = 0

    if len(gameState.PlayerBody) < gameState.PlayerSize:
        # gameState.PlayerBody.append([gameState.PlayerHead[0], gameState.PlayerHead[1]])
        gameState.PlayerBody.insert(0, [gameState.PlayerHead[0], gameState.PlayerHead[1]])
    else:
        gameState.PlayerBody.pop()
        gameState.PlayerBody.insert(0, [gameState.PlayerHead[0], gameState.PlayerHead[1]])


    for part in gameState.PlayerBody:
        gameState.grid[part[0]][part[1]] = 1
    gameState.grid[gameState.PlayerHead[0]][gameState.PlayerHead[1]] = 3


def checkBoundary():
    if MAP_LOOP:
        if gameState.PlayerHead[0] > len(gameState.grid) - 1:
            gameState.PlayerHead[0] = 0
            gameState.PlayerBody[0] = [0, gameState.PlayerHead[1]]
        if gameState.PlayerHead[0] < 0:
            gameState.PlayerHead[0] = len(gameState.grid) - 1
            gameState.PlayerBody[0] = [len(gameState.grid) - 1, gameState.PlayerHead[1]]
        if gameState.PlayerHead[1] > len(gameState.grid) - 1:
            gameState.PlayerHead[1] = 0
            gameState.PlayerBody[0] = [gameState.PlayerHead[0], 0]
        if gameState.PlayerHead[1] < 0:
            gameState.PlayerHead[1] = len(gameState.grid) - 1
            gameState.PlayerBody[0] = [gameState.PlayerHead[0], len(gameState.grid) - 1]
    else:
        if gameState.PlayerHead[0] > len(gameState.grid) - 1:
            return True
        if gameState.PlayerHead[0] < 0:
            return True
        if gameState.PlayerHead[1] > len(gameState.grid) - 1:
            return True
        if gameState.PlayerHead[1] < 0:
            return True
    return False


def checkCollision():
    for i in range(1, len(gameState.PlayerBody)):
        if gameState.PlayerHead == gameState.PlayerBody[i]:
            return True
    return False
    

def getGridPosColor(pos):
    if gameState.grid[pos[0]][pos[1]] == 0:
        # Empty
        return WHITE
    if gameState.grid[pos[0]][pos[1]] == 1:
        # Player Body
        return GREEN
    if gameState.grid[pos[0]][pos[1]] == 2:
        # Food
        return RED
    if gameState.grid[pos[0]][pos[1]] == 3:
        # Player Head
        return BLACK


def movePlayer(key):
    if key[playerMoves[0]] or key[playerMoves[1]] or key[playerMoves[2]] or key[playerMoves[3]]:
        if key[playerMoves[0]]:
            gameState.PlayerHead[0] -= 1
            gameState.movementDirection = [-1, 0]
        elif key[playerMoves[1]]:
            gameState.PlayerHead[0] += 1
            gameState.movementDirection = [1, 0]
        elif key[playerMoves[2]]:
            gameState.PlayerHead[1] -= 1
            gameState.movementDirection = [0, -1]
        elif key[playerMoves[3]]:
            gameState.PlayerHead[1] += 1
            gameState.movementDirection = [0, 1]
    else:
        gameState.PlayerHead[0] += gameState.movementDirection[0]
        gameState.PlayerHead[1] += gameState.movementDirection[1]

def checkFoodEaten():
    if gameState.grid[gameState.PlayerHead[0]][gameState.PlayerHead[1]] == 2:
        gameState.FoodSpawned -= 1
        gameState.PlayerSize += 1
        gameState.grid[gameState.PlayerHead[0]][gameState.PlayerHead[1]] = 3

def drawGrid():
    for x in range(0, screenSize[0], blockSize):
        for y in range(0, screenSize[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            
            pygame.draw.rect(screen,  getGridPosColor((x//blockSize,y//blockSize)), rect, 0)
            pygame.draw.rect(screen, BLACK, rect, 1)


def spawnFood():
    if gameState.FoodSpawned < MAX_FOOD:
        while gameState.FoodSpawned < MAX_FOOD:
            random_x = round(random.randint(0, len(gameState.grid) - 1))
            random_y = round(random.randint(0, len(gameState.grid) - 1))

            if gameState.grid[random_x][random_y] != 0:
                continue

            gameState.grid[random_x][random_y] = 2
            gameState.FoodSpawned += 1


def main():  
 
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False  
        
        # Movement
        key = pygame.key.get_pressed()  
        movePlayer(key)

        if checkBoundary():
            print("Game Over")
            break

        spawnFood()
        checkFoodEaten()

        

        movePlayerBody()

        # ! Draw
        screen.fill(bg)  
        drawGrid()
        
        # Check for self collisions
        if checkCollision():
            print("Game Over")
            break

        pygame.display.update()  
        clock.tick(fps)  

    # ! Game Over
    font = pygame.font.SysFont('arial', 40)
    gameOver = font.render("Game Over", True, RED)
    screen.blit(gameOver, (screenSize[0]/2 - gameOver.get_width()/2, screenSize[1]/2 - gameOver.get_height()/2))
    pygame.display.update()

    # Close the window and quit.
    pygame.quit()  
    sys.exit  


if __name__ == '__main__':
    main()