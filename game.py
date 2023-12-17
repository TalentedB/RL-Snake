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
        self.image = pygame.Surface([20, 20])  
        self.image.fill(GREEN)  
        self.rect = self.image.get_rect()  
        self.rect.center = pos  

class FoodSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([20, 20])  
        self.image.fill(RED)  
        self.rect = self.image.get_rect()  
        self.rect.center = pos

class GameState:
    def __init__(self, gridSize):
        self.grid = [[0 for x in range(gridSize)] for y in range(gridSize)]
        self.PlayerSize = 1

pygame.init()  
clock = pygame.time.Clock()  
fps = 50
bg = [0, 0, 0]  
screenSize =[600, 600]  
screen = pygame.display.set_mode(screenSize)  
player = Sprite([40, 50])  
# Define keys for player movement  
player.move = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]  
player.vx = 5  
player.vy = 10

blockSize = 20
gridSize = int(screenSize[0] // blockSize)
gameState = GameState(gridSize)
food_group = pygame.sprite.Group() 

def drawGrid():
    for x in range(0, screenSize[0], blockSize):
        for y in range(0, screenSize[1], blockSize):
            rect = pygame.Rect(x, y, blockSize, blockSize)

            pygame.draw.rect(screen, getGridPosColor((x//blockSize,y//blockSize)), rect, 1)
            if random.randint(0, 100) == 1:
                food = FoodSprite([x, y])  
                food_group.add(food)  
            

def getGridPosColor(pos):
    if gameState.grid[pos[0]][pos[1]] == 0:
        return WHITE
    if gameState.grid[pos[0]][pos[1]] == 1:
        return GREEN
    if gameState.grid[pos[0]][pos[1]] == 2:
        return RED

def main():  
 
    # Add random food
    for i in range(10):
        random_x = random.randint(0, screenSize[0])
        random_y = random.randint(0, screenSize[1])
        food = FoodSprite([random_x, random_y])  
        food_group.add(food)  
  
    player_group = pygame.sprite.Group()  
    player_group.add(player)  
  
    while True:  
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  
                return False  
        key = pygame.key.get_pressed()  
        for i in range(2):  
            if key[player.move[i]]:  
                player.rect.x += player.vx * [-1, 1][i]  
  
        for i in range(2):  
            if key[player.move[2:4][i]]:  
                player.rect.y += player.vy * [-1, 1][i]  
        screen.fill(bg)  
        drawGrid()
        # first parameter takes a single sprite  
        # second parameter takes sprite groups  
        # third parameter is a kill command if true  
        food_hit = pygame.sprite.spritecollide(player, food_group, True)  
        if food_hit:
            gameState.PlayerSize += 1
            print("Player size: " + str(gameState.PlayerSize))


        player_group.draw(screen)  
        food_group.draw(screen)  
        pygame.display.update()  
        clock.tick(fps)  
    pygame.quit()  
    sys.exit  
if __name__ == '__main__':
    main()