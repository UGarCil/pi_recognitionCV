# MODULES

import torch
import random 
import numpy as np 
from constants import *
from Game import Game
from collections import deque
from Snake import Bp
from model import LQnet,QTrainer
from plotHelper import plot
# DD.

MAX_MEMORY = 200_000
BATCH_SIZE = 1500
LR = 0.001

# DD. AGENT
# agent = Agent()
# interp. the main element that will control the Game and the model making predictions
class Agent():
    def __init__(self):
        self.numberGames = 0
        self.epsilon = 0 #controls the randomness in the model training strategy
        self.gamma = 0.9 #controls the discount rate; how much importance the model gives to subsequent outcomes
        self.memory = deque(maxlen=MAX_MEMORY) #deque automatically removes elements from the left, keeping newest elements
        self.lr = LR
        self.model = LQnet(11,256,3)
        self.trainer = QTrainer(self.model,self.lr,self.gamma)
    
    def get_state(self,game):
        # get the head of the snake and use it as reference
        # to create floating heads that will evaluate danger
        # in each of the 4 cardinal directions
        head = game.snake.body[-1]
        _,danger_r = game.isGameOver(snakeHead = Bp(head.c+1,head.r))
        _,danger_d = game.isGameOver(snakeHead = Bp(head.c,head.r+1))
        _,danger_l = game.isGameOver(snakeHead = Bp(head.c-1,head.r))
        _,danger_u = game.isGameOver(snakeHead = Bp(head.c,head.r-1))
        
        dir_r = game.snake.direction == RIGHT
        dir_d = game.snake.direction == DOWN
        dir_l = game.snake.direction == LEFT
        dir_u = game.snake.direction == UP
        
        state = [
            # Danger straight
            (dir_r and danger_r) or
            (dir_d and danger_d) or
            (dir_l and danger_l) or
            (dir_u and danger_u),
            
            # Danger right
            (dir_r and danger_d) or
            (dir_d and danger_l) or
            (dir_l and danger_u) or
            (dir_u and danger_r),
            
            # Danger left
            (dir_r and danger_u) or
            (dir_d and danger_r) or
            (dir_l and danger_d) or
            (dir_u and danger_l),
            
            # move direction
            dir_r,
            dir_d,
            dir_l,
            dir_u,
            
            # Food location 
            game.snake.fd.c > head.c, #food right
            game.snake.fd.r > head.r, #food down
            game.snake.fd.c < head.c, #food left
            game.snake.fd.r < head.r #food up
            # game.snake.fd.c == head.c, #food straight
            # game.snake.fd.r == head.r #food straight
            
        ]
        
        return np.array(state,dtype=int)
    

    def remember(self,state,action,reward,next_state,done):
        _agent_env = (state,action,reward,next_state,done)
        self.memory.append(_agent_env)
    
    def train_long(self):
        if len(self.memory) > BATCH_SIZE:
            mini_batch = random.sample(self.memory,BATCH_SIZE)
        else:
            mini_batch = self.memory
            
        states, actions,rewards,next_states,dones = zip(*mini_batch)
        self.trainer.train_step(states,actions,rewards,next_states,dones)
        
    def train_short(self,state,action,reward,next_state,done):
        self.trainer.train_step(state,action,reward,next_state,done)
    
    def get_action(self, state):
        # random moves: tradeoff exploration/exploitation
        # the more games, the smaller epsilon
        self.epsilon = 80 - self.numberGames
        # final_move = [0,0,0]
        # if a random number is less than epsilon, then use randomness
        if random.randint(0,200) < self.epsilon:
            idx = random.randint(0,2)
        else:
            state0 = torch.tensor(state,dtype=torch.float)
            prediction = self.model(state0)
            # print(prediction)
            # Get the index of the maximum value
            idx = torch.argmax(prediction).item()
        return int(idx)
    
# FD. train()
# purp. train the agent
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = Game()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)

        # train short memory
        agent.train_short(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            game.reset()
            agent.numberGames += 1
            agent.train_long()

            if score > record:
                record = score
                agent.model.save()
                print("model saved")

            print('Game', agent.numberGames, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.numberGames
            plot_mean_scores.append(mean_score)
            # plot(plot_scores, plot_mean_scores)  

if __name__ == "__main__":
    train()

