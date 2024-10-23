# MODULES

from constants import *
from Snake import Snake

# DD
# DD. GAME
# game = Game()
# interp. a game that will be controlled by an AI Agent 
class Game():
    def __init__(self):
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.snake = Snake()
        self.iteration = 0
        self.score = 0
    
    def draw(self):
        display.fill("#1e1e1e")
        self.snake.draw(display)
        pygame.display.flip()
        self.clock.tick(FPS)
        
    def play_step(self,idx):
        [pygame.quit() for event in pygame.event.get() if event.type == pygame.QUIT]
        reward = 0
        score = 0
        
        # Move snake and update head
        self.snake.updateDirection(idx)
        self.snake.move()
        rewardIfGO,done = self.isGameOver()
        if not done:
            rewardFood,score = self.snake.updateFoodInteraction()
            reward = rewardFood + rewardIfGO
        else:
            score = 0
            reward = rewardIfGO
        self.iteration += 1
        self.score += score
        self.draw()
        return reward,done,self.score
    
    def isGameOver(self,snakeHead = None):
        if snakeHead is None:
            # snake head touches walls
            snakeHead = self.snake.body[-1]

        if snakeHead.c <0 or snakeHead.c > DIMS[0]-1 or snakeHead.r <0 or snakeHead.r > DIMS[1]-1:
            return GAMEOVER_PENALTY,True
        
        for bp in self.snake.body:
            if bp != snakeHead:
                if bp.rect.colliderect(snakeHead):
                    return GAMEOVER_PENALTY,True
        if self.iteration > 100 * (len(self.snake.body)):
            return IDLE_PENALTY,True
        
        return 0,False
    
# CODE

if __name__ == "__main__":
    game = Game()
    while True:
        game.draw()
        game.play_step(random.randint(0,2))
        reward,gameOver = game.isGameOver()
        print(game.iteration)
        if gameOver:
            print(reward)
            game.reset()