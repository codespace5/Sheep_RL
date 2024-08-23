from turtle import Screen
import numpy as np
import pygame
from time import time, sleep
from random import randint as r
import random

n = 5
scrax = n*10
scray = n*10
background = (51,51, 51)
screen = pygame.display.set_mode((scrax, scray))
colors = [(51, 51, 51) for i in range(n**2)]
reward = np.zeros((n,n))
# colors[51*23+ 25] = (255, 0, 0)
# colors[51*24+ 25] = (255, 0, 0)
# colors[51*25+ 25] = (255, 0, 0)
# colors[51*25+ 26] = (255, 0, 0)
# colors[51*24+ 27] = (255, 0, 0)
# colors[51*23+ 27] = (255, 0, 0)
# colors[51*25+ 27] = (255, 0, 0)
states = {}
actions = {"up": 0,"down" : 1,"left" : 2,"right" : 3}
terminals = []
penalities = 7
Q = np.zeros((n**2,4))
while penalities != 0:
    i = r(0,n-1)
    j = r(0,n-1)
    if reward[i,j] == 0 and [i,j] != [0,0] and [i,j] != [n-1,n-1]:
        reward[i,j] = -1
        penalities-=1
        colors[n*i+j] = (255,0,0)
        terminals.append(n*i+j)
reward[n-1,n-1] = 1
colors[n**2 - 1] = (0,255,0)
terminals.append(n**2 - 1)
k = 0
for i in range(n):
    for j in range(n):
        states[(i,j)] = k
        k+=1
alpha = 0.01
gamma = 0.9
current_pos = [0,0]
epsilon = 0.25


def select_action(current_state):
    global current_pos,epsilon
    possible_actions = []
    if np.random.uniform() <= epsilon:
        if current_pos[0] != 0:
            possible_actions.append("up")
        if current_pos[0] != n-1:
            possible_actions.append("down")
        if current_pos[1] != 0:
            possible_actions.append("left")
        if current_pos[1] != n-1:
            possible_actions.append("right")
        action = actions[possible_actions[r(0,len(possible_actions) - 1)]]
    else:
        m = np.min(Q[current_state])
        if current_pos[0] != 0: #up
            possible_actions.append(Q[current_state,0])
        else:
            possible_actions.append(m - 100)
        if current_pos[0] != n-1: #down
            possible_actions.append(Q[current_state,1])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != 0: #left
            possible_actions.append(Q[current_state,2])
        else:
            possible_actions.append(m - 100)
        if current_pos[1] != n-1: #right
            possible_actions.append(Q[current_state,3])
        else:
            possible_actions.append(m - 100)
        action = random.choice([i for i,a in enumerate(possible_actions) if a == max(possible_actions)]) #randomly selecting one of all possible actions with maximin value
    print(action)
    return action
      
      
def episode():
    global current_pos,epsilon
    current_state = states[(current_pos[0],current_pos[1])]
    action = select_action(current_state)
    if action == 0: #move up
        current_pos[0] -= 1
    elif action == 1: #move down
        current_pos[0] += 1
    elif action == 2: #move left
        current_pos[1] -= 1
    elif action == 3: #move right
        current_pos[1] += 1
    new_state = states[(current_pos[0],current_pos[1])]
    if new_state not in terminals:
        Q[current_state,action] += alpha*(reward[current_pos[0],current_pos[1]] + gamma*(np.max(Q[new_state])) - Q[current_state,action])
    else:
        Q[current_state,action] += alpha*(reward[current_pos[0],current_pos[1]] - Q[current_state,action])
        current_pos = [0,0]
        if epsilon > 0.05:
            epsilon -= 3e-4 #reducing as time increases to satisfy Exploration & Exploitation Tradeoff
            
       
def layout():
    c =0
    for i in range(0, scrax, 10):
        for j in range(0, scray, 10):
            pygame.draw.rect(screen, (255, 255, 255),(j, i, j+10, i+10),0)
            pygame.draw.rect(screen, colors[c], (j+2, i+2, j+8, i+8), 0)
            c+= 1
            


run = True
for i in range(100000):
    episode()
    print("train")
    print(epsilon)
current_pos = [0,0]
while run:
    screen.fill(background)
    layout()
    print("2131231231232",current_pos)
    pygame.draw.circle(screen,(25,129,230),(current_pos[1]*10 + 5,current_pos[0]*10 + 5),3,0)
    pygame.display.flip()
    episode()
pygame.quit()