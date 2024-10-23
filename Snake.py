from constants import *

# DD. BODY_PART
# bp = Bp()
# interp.basic cloks unit that makes the snake's body
class Bp():
    def __init__(self,c,r):
        self.c = c 
        self.r = r
        self.color = "green"
        self.updateRect()
        

    def updateRect(self):
        self.x = self.c * RES 
        self.y = self.r * RES
        self.rect = pygame.Rect(self.x, self.y, RES, RES)
        
    def draw(self,display):
        pygame.draw.rect(display,self.color,self.rect)

# DD. FOOD
# fd = Food()
# interp. object representing the goal for the snake to eat
class Food():
    def __init__(self):
        self.first = True
        self.reset()
        
    def updateRect(self):
        self.x = self.c * RES 
        self.y = self.r * RES 
        self.rect = pygame.Rect(self.x, self.y, RES, RES)
    
    def draw(self,display):
        pygame.draw.rect(display,"white",self.rect)
    
    def reset(self):
        # if self.first:
        #     self.c = DIMS[0]-12
        #     self.r = DIMS[1]-12
        #     self.first = False
        # else:
        self.c = random.randint(0,DIMS[0]-1) 
        self.r = random.randint(0,DIMS[1]-1)
        self.updateRect()

# DD. SNAKE
# snake = Snake()
# interp. an object representing the snake (contains main algorithm)
class Snake():
    def __init__(self):
        self.reset()
        
        
    def move(self):
        head = self.body[-1]
        _hc = head.c
        _hr = head.r
        if self.direction == RIGHT:
            newHead = Bp(_hc+1,_hr)
        elif self.direction == DOWN:
            newHead = Bp(_hc,_hr+1)
        elif self.direction == LEFT:
            newHead = Bp(_hc-1,_hr)
        elif self.direction == UP:
            newHead = Bp(_hc,_hr-1)
            
        self.body.append(newHead)
    
    def updateFoodInteraction(self):
        if self.body[-1].rect.colliderect(self.fd):
            reward = FOOD_REWARD
            score = 1
            self.fd.reset()
        else:
            reward = 0
            score = 0
            self.body.pop(0)
            
        return reward,score
        
        
    def updateDirection(self,action):
        # action is one of:
        # 0 for left relative to snake head
        # 1 for stay in current direction
        # 2 for right relative to snake head
        
        # find the position of 1 in the direction
        _idx = self.direction.index(1)
        _new_direction = [0,0,0,0]
        # depending on the action, move it to the right or left of the current self.direction
        if action == 0:
            _new_direction[(_idx-1)%4] = 1
            self.direction = _new_direction
        elif action == 2:
            _new_direction[(_idx+1)%4] = 1
            self.direction = _new_direction
        else:
            self.direction = self.direction
    
        
            
    def reset(self):
        _halfScreen = (DIMS[0]//2,DIMS[1]//2 )
        bp_head = Bp(_halfScreen[0],_halfScreen[1])
        bp2 = Bp(_halfScreen[0]-1,_halfScreen[1])
        bp1 = Bp(_halfScreen[0]-2,_halfScreen[1])
        # bp4 = Bp(13,10)
        self.body = [bp1,bp2,bp_head]
        self.direction = RIGHT
        self.fd = Food()
        self.head = self.body[-1]
        # self.score = 0
    
    def draw(self,display):
        self.fd.draw(display)
        for idx,bp in enumerate(self.body):
            if idx == len(self.body)-1:
                bp.color = "red"
            else:
                bp.color = "green"
            bp.draw(display)
        
      
