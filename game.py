import pygame  
import sys  
import random
#Sprite class   

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

class Sprite(pygame.sprite.Sprite):  
    def __init__(self, pos):  
        pygame.sprite.Sprite.__init__(self)  
        self.image = pygame.Surface([blockSize, blockSize])  
        self.image.fill(GREEN)  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  

class FoodSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([blockSize, blockSize])  
        self.image.fill(RED)  
        self.rect = self.image.get_rect()  
        self.rect.center = pos

class GameState:
    def __init__(self, gridSize):
        self.grid = [[0 for x in range(gridSize)] for y in range(gridSize)]
        self.PlayerSize = 1
        self.movementDirection = [1, 0]
        self.PlayerBody = [(0, 0)]
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
food_group = pygame.sprite.Group() 



player = Sprite([blockSize/2, blockSize/2])  

# Define keys for player movement  
player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
player.vx = blockSize
player.vy = blockSize



print("Screen size: " + str(screenSize))
print("Block size: " + str(blockSize))

print("Grid size: " + str(gridSize))


def drawGrid():
    for x in range(0, screenSize[0], blockSize):
        for y in range(0, screenSize[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)

            pygame.draw.rect(screen, getGridPosColor((x//blockSize,y//blockSize)), rect, 1)



def spawnFood():
    if gameState.FoodSpawned == 0:
        random_x = round(random.randint(0, screenSize[0] - 1))//blockSize * blockSize
        random_y = round(random.randint(0, screenSize[1] - 1))//blockSize * blockSize
        # print("Random x: " + str(random_x) + " Random y: " + str(random_y))

        gameState.grid[random_x//blockSize][random_y//blockSize] = 2
        gameState.FoodSpawned = 1

        food = FoodSprite([random_x + blockSize/2, random_y + blockSize/2])  
        food_group.add(food)


def movePlayerBody():
    for i in range(len(gameState.PlayerBody)):
        if i == 0:
            gameState.PlayerBody[i] = (player.rect.x, player.rect.y)
        else:
            gameState.PlayerBody[i] = gameState.PlayerBody[i-1]
    if gameState.FoodSpawned == 0:
        gameState.PlayerBody.append(gameState.PlayerBody[-1])
        # gameState.PlayerBody.pop()
    
    print(gameState.PlayerBody)


def getGridPosColor(pos):
    if gameState.grid[pos[0]][pos[1]] == 0:
        # return [WHITE, RED][random.randint(0, 1)]
        return WHITE
    if gameState.grid[pos[0]][pos[1]] == 1:
        return GREEN
    if gameState.grid[pos[0]][pos[1]] == 2:
        return RED

def movePlayer(key):
    if key:
        if key[player.move[0]]:
            player.rect.x -= player.vx
            gameState.movementDirection = [-1, 0]
        elif key[player.move[1]]:
            player.rect.x += player.vx
            gameState.movementDirection = [1, 0]
        elif key[player.move[2]]:
            player.rect.y -= player.vy
            gameState.movementDirection = [0, -1]
        elif key[player.move[3]]:
            player.rect.y += player.vy
            gameState.movementDirection = [0, 1]
    else:
        player.rect.x += player.vx * gameState.movementDirection[0]
        player.rect.y += player.vy * gameState.movementDirection[1]


def main():  
 
    player_group = pygame.sprite.Group()  
    player_group.add(player)  
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False  
        
        # Movement
        key = pygame.key.get_pressed()  
        movePlayer(key)
        
        # Draw
        screen.fill(bg)  
        drawGrid()
        movePlayerBody()
        spawnFood()
        

        # Check for collisions
        food_hit = pygame.sprite.spritecollide(player, food_group, True)  
        if food_hit:
            gameState.PlayerSize += 1
            gameState.FoodSpawned = 0
            print(food_hit[0].rect.center)
            # print("Player size: " + str(gameState.PlayerSize))


        player_group.draw(screen)  
        food_group.draw(screen) 

        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  


if __name__ == '__main__':
    main()