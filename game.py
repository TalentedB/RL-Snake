import pygame  
import sys  
import random
#Sprite class   

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

MAX_FOOD = 1
PLAYER_SPAWN = [2, 0]

class GameState:
    def __init__(self, gridSize):
        self.grid = [[0 for x in range(gridSize)] for y in range(gridSize)]
        self.PlayerSize = 1
        self.movementDirection = [0, 1]
        self.PlayerBody = [PLAYER_SPAWN]
        self.PlayerHead = PLAYER_SPAWN
        self.FoodSpawned = 0

pygame.init()  
clock = pygame.time.Clock()  
fps = 5
bg = [0, 0, 0]  
screenSize =[600, 600]  
screen = pygame.display.set_mode(screenSize)  

blockSize = 50
gridSize = int(screenSize[0] // blockSize)
gameState = GameState(gridSize)



# Define keys for player movement  
playerMoves = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  



# print("Screen size: " + str(screenSize))
# print("Block size: " + str(blockSize))

# print("Grid size: " + str(gridSize))


def drawGrid():
    for x in range(0, screenSize[0], blockSize):
        for y in range(0, screenSize[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)
            
            pygame.draw.rect(screen,  getGridPosColor((x//blockSize,y//blockSize)), rect, 0)
            pygame.draw.rect(screen, BLACK, rect, 1)




def spawnFood():
    if gameState.FoodSpawned < MAX_FOOD:
        while True:
            random_x = round(random.randint(0, len(gameState.grid) - 1))
            random_y = round(random.randint(0, len(gameState.grid) - 1))

            if gameState.grid[random_x][random_y] != 0:
                continue

            gameState.grid[random_x][random_y] = 2
            gameState.FoodSpawned += 1
            break




def movePlayerBody():

    tail = gameState.PlayerBody[-1]

    if len(gameState.PlayerBody) == 1:
        tail = (gameState.PlayerHead[0] - gameState.movementDirection[0], gameState.PlayerHead[1] - gameState.movementDirection[1])
    else:
        tail = gameState.PlayerBody[-1]

    for i in range(len(gameState.PlayerBody) - 1, 0, -1):
        gameState.PlayerBody[i] = gameState.PlayerBody[i-1]

    gameState.PlayerBody[0] = gameState.PlayerHead
    gameState.grid[gameState.PlayerHead[0]][gameState.PlayerHead[1]] = 1

    if gameState.FoodSpawned == 0:
        gameState.PlayerBody.append(tail)
        gameState.grid[tail[0]][tail[1]] = 1
    else:
        print("Tail: " + str(tail))
        gameState.grid[tail[0]][tail[1]] = 0

    print(gameState.PlayerBody)


def checkBoundary():
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


def checkCollision():
    for i in range(1, len(gameState.PlayerBody)):
        if gameState.PlayerHead == gameState.PlayerBody[i]:
            return True
    return False
    

def getGridPosColor(pos):
    if gameState.grid[pos[0]][pos[1]] == 1:
        # print("Player head: " + str(gameState.PlayerHead))
        return GREEN
    if gameState.grid[pos[0]][pos[1]] == 0:
        # return [WHITE, RED][random.randint(0, 1)]
        return WHITE
    if gameState.grid[pos[0]][pos[1]] == 2:
        return RED


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
        return True
    return False
def main():  
 
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False  
        
        # Movement
        key = pygame.key.get_pressed()  
        movePlayer(key)
        spawnFood()
        if checkFoodEaten():
            gameState.PlayerSize += 1
            gameState.FoodSpawned -= 1
            print("Food eaten")
        
        checkBoundary()
        movePlayerBody()
        
        # Draw
        screen.fill(bg)  
        drawGrid()
        
        
        
        # Check for collisions
        

        if checkCollision():
            print("Game Over")
            # return 0

        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  


if __name__ == '__main__':
    main()