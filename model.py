# MODULES
import torch 
import torch.nn as nn
import torch.optim as optim 
import torch.nn.functional as F
import os 

# DD

# DD. LINEAR_QNET
# lQ = LQnet()
# interp. 
class LQnet(nn.Module):
    def __init__(self,input_size, hidden_size, output_size=3):
        super().__init__()
        self.block1 = nn.Sequential(
            nn.Linear(input_size,hidden_size),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_size,hidden_size//2),
            nn.ReLU(inplace=True),
            nn.Linear(hidden_size//2,output_size),
            # nn.ReLU(inplace=True),
            # nn.Linear(hidden_size//2,hidden_size//2),
            # nn.ReLU(inplace=True),
            # nn.Linear(hidden_size//2,output_size),
            # nn.Softmax()
        )
    
    def forward(self,x):
        x = self.block1(x)
        return x
    
    def save(self,file_name= "model.pth"):
        model_folder_path = "./model"
        if not os.path.exists(model_folder_path):
            os.mkdir(model_folder_path)
        file_name = os.path.join(model_folder_path,file_name)
        torch.save(self.state_dict(),file_name)
    
    
# DD. QTrainer
# qt = QTrainer()
# interp. an object that actually uses the model to train the network

class QTrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.gamma = gamma
        self.model = model
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)
        self.criterion = nn.MSELoss()

    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(state, dtype=torch.float)
        # print(state)
        next_state = torch.tensor(next_state, dtype=torch.float)
        action = torch.tensor(action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)
        # (n, x)

        if len(state.shape) == 1:
            # (1, x)
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # 1: predicted Q values with current state
        pred = self.model(state)

        target = pred.clone()
        for idx in range(len(done)):
            Q_new = reward[idx]
            if not done[idx]:
                Q_new = reward[idx] + self.gamma * torch.max(self.model(next_state[idx]))
            # rather than passing:
            # target[idx][torch.argmax(action[idx]).item()] = Q_new
            # which finds the index of a vector of shape [int,int,int],
            # we pass the action directly, as it is a tensor with a single scalar in GCU's version of the program
            target[idx][action[idx].item()] = Q_new
    
        # 2: Q_new = r + y * max(next_predicted Q value) -> only do this if not done
        # pred.clone()
        # preds[argmax(action)] = Q_new
        self.optimizer.zero_grad()
        loss = self.criterion(target, pred)
        loss.backward()

        self.optimizer.step()    
        
        

# CODE