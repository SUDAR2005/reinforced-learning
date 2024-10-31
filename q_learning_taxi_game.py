#import necessary libraries
import numpy as np
import gym
import random as rand

#initialize environment and render initial state
env=gym.make('Taxi-v3',render_mode='ansi')
env.reset()
env.render()

# Hyperparameters
total_episode = 10000        
total_test_episode = 100
max_steps = 100
lr = 0.1
gamma = 0.95

# Exploration parameters
epsilon = 1.0
max_epsilon = 1.0
min_epsilon = 0.01
decay_rate = 0.001

#initialize the Q-table with zeros
action_size=env.action_space.n
state_size=env.observation_space.n
q_table=np.zeros((state_size,action_size))

#training phase
for episode in range(total_episode):
    state=env.reset()[0]
    done=False
    
    for step in range(max_steps):
        exp_exp_tradeoff=rand.uniform(0,1)
        
        #select action using epsilon-greedy strategy
        if exp_exp_tradeoff > epsilon:
            action=np.argmax(q_table[state,:])
        else:
            action=env.action_space.sample()
        #take action and observe the result
        new_state,reward,terminated,truncated,info=env.step(action)
        done=terminated or truncated
        #update Q-table
        q_table[state,action]=q_table[state,action]+lr*(reward+gamma*np.max(q_table[new_state,:])-q_table[state,action])
        state=new_state
        if done:
            break
    #decay epsilon after each episode
    epsilon=min_epsilon+(max_epsilon-min_epsilon)*np.exp(-decay_rate*episode)
print("Final Q-Table:")
print(q_table)
#testing phase
rewards=[]
for episode in range(total_test_episode):
    state=env.reset()[0]
    done=False
    total_rewards=0
    
    print('=========================')
    print('EPISODE:',episode)
    
    for step in range(max_steps):
        env.render()
        action=np.argmax(q_table[state,:])
        new_state,reward,terminated,truncated,info=env.step(action)
        done=terminated or truncated
        total_rewards += reward
        if done:
            rewards.append(total_rewards)
            print('Score:',total_rewards)
            break
        state=new_state

env.close()
print('Average Score Over Time:',sum(rewards)/total_test_episode)