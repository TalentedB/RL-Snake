import game


gameState = game.GameState(20, [600, 600], 10, 10)
gameState.runGame()

gameState.printGrid()

print(gameState.board)

