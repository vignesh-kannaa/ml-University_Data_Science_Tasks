import enum
import random

def _is_terminal(pos):
    return pos == [4,3] or pos == [4,2]

def _stochastic_action(chosen_action):
    true_action = chosen_action
    if chosen_action == Move.up or chosen_action == Move.down:
        r = random.randint(0,9)
        if r == 0:
            true_action = Move.right
        elif r == 1:
            true_action = Move.left
    if chosen_action == Move.right or chosen_action == Move.left:
        r = random.randint(0,9)
        if r == 0:
            true_action = Move.up
        elif r == 1:
            true_action = Move.down
    return true_action

def _bounded_move(frm,to):
    if to[0] < 1:
        to[0] = 1
    elif to[0] > 4:
        to[0] = 4
    elif to[1] < 1:
        to[1] = 1
    elif to[1] > 3:
        to[1] = 3
    elif to == [2,2]:
        to = frm 
    return to

def _move(pos,chosen_action):
    #_move should not be called in terminal states
    assert not _is_terminal(pos)

    #action modified with probability 0.2
    true_action = _stochastic_action(chosen_action)

    #make a candidate move
    if true_action == Move.up:
        candidate_pos = [pos[0],pos[1]+1]
    elif true_action == Move.right:
        candidate_pos = [pos[0]+1,pos[1]]
    elif true_action == Move.down:
        candidate_pos = [pos[0],pos[1]-1]
    elif true_action == Move.left:
        candidate_pos = [pos[0]-1,pos[1]]

    #prevent the candidate move from moving out of bounds
    next_pos = _bounded_move(pos,candidate_pos)

    #return the new position and the reward for the current state
    non_terminal_reward = -0.04
    return (next_pos,non_terminal_reward)

def _terminal_reward(pos):
    #terminal reward should only be called in a terminal state
    assert _is_terminal(pos)

    if pos == [4,3]:
        return 1
    else:
        return -1

class Move(enum.Enum):
    up = 0
    right = 1
    down = 2
    left = 3

def run_policy(start_pos,policy):
    positions = []
    rewards = []

    #while non-terminal, move according to the policy, recording positions and
    #rewards.
    current_pos = start_pos
    while not _is_terminal(current_pos):
      positions.append(current_pos)
      action = policy(current_pos)
      (current_pos,reward) = _move(current_pos,action)
      rewards.append(reward)
    
    #record the final terminal postion and reward
    positions.append(current_pos)
    rewards.append(_terminal_reward(current_pos))

    return positions,rewards

def random_pos():
    pos = [random.randint(1,4),random.randint(1,3)]
    if(pos == [2,2]):
        return random_pos()
    else:
        return pos

def sample_policy(pos):
    #In the bottom right position, move left
    if(pos == [4,1]):
      return Move.left
    #In the top row, move right
    elif(pos[1] == 3):
      return Move.right
    #Otherwise, move up
    else:
      return Move.up

print(run_policy(random_pos(),sample_policy))

