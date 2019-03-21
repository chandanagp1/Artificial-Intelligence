import numpy as np
import json
fd=open('input2.txt','r')

n=int(fd.readline().rstrip())
nc=int(fd.readline().rstrip())
no=int(fd.readline().rstrip())
gamma=0.9
epsilon=0.1
obst=[]
for i in range(no):
    str1 = fd.readline().rstrip()
    str1 = str1.split(',')
    tup = (int(str1[0]), int(str1[1]))
    obst.append(tup)
# print obst

cars_start=[]
for i in range(nc):
    str1=fd.readline().rstrip()
    str1 = str1.split(',')
    tup = (int(str1[0]), int(str1[1]))
    cars_start.append(tup)
# print cars_start

cars_end=[]
for i in range(nc):
    str1=fd.readline().rstrip()
    str1 = str1.split(',')
    tup=(int(str1[0]),int(str1[1]))
    cars_end.append(tup)
# print cars_end

table=[]
transition_array=[]
Rewards_array=[]

for car_index in range(nc):
    Transitions = {}
    Reward = {}
    for i in range(n):
        for j in range(n):
            tup=(i,j)
            r=(min(n-1,i+1),j)
            l=(max(0,i-1),j)
            d=(i,min(n-1,j+1))
            u=(i,max(0,j-1))
            di = {}
            if tup!=cars_end[car_index]:
                di['R']=[(r,0.7),(l,0.1),(d,0.1),(u,0.1)]
                di['L']=[(l,0.7),(r,0.1),(d,0.1),(u,0.1)]
                di['U']=[(u,0.7),(l,0.1),(r,0.1),(d,0.1)]
                di['D']=[(d,0.7),(r,0.1),(l,0.1),(u,0.1)]

            else:
                # print 'trs car end=',tup
                di['R']=[(r,0),(l,0),(d,0),(u,0)]
                di['L']=[(l,0),(r,0),(d,0),(u,0)]
                di['U']=[(u,0),(l,0),(r,0),(d,0)]
                di['D']=[(d,0),(r,0),(l,0),(u,0)]

#             # print di
            Transitions[tup]=di


            if tup in obst:
                Reward[tup]=-101
            elif tup==cars_end[car_index]:
                Reward[tup]=99
            else:
                Reward[tup]=-1

    Rewards_array.append(Reward)
    transition_array.append(Transitions)


class MarkovDecisionProcess:

    """A Markov Decision Process, defined by an states, actions, transition model and reward function."""

    def __init__(self, transition={}, reward={}, gamma=.9):
        #collect all nodes from the transition models
        self.states = transition.keys()
        #initialize transition
        self.transition = transition
        #initialize reward
        self.reward = reward
        #initialize gamma
        self.gamma = gamma

    def R(self, state):
        """return reward for this state."""
        return self.reward[state]

    def actions(self, state):
        """return set of actions that can be performed in this state"""
        return self.transition[state].keys()

    def T(self, state, action):
        """for a state and an action, return a list of (probability, result-state) pairs."""
        return self.transition[state][action]

#Initialize the MarkovDecisionProcess object
def value_iteration(mdp):
    """
    Solving the MDP by value iteration.
    returns utility values for states after convergence
    """
    states = mdp.states
    actions = mdp.actions
    T = mdp.T
    R = mdp.R
    # V1=R
    V1 = {s: R(s) for s in states}
    while True:
        V = V1.copy()
        delta = 0
        for s in states:
            sums=[]
            for a in actions(s):
                sum=0
                for (s1,p) in T(s,a):
                    sum=np.float64(sum+p*V[s1])
                sums.append(sum)
            V1[s]=np.float64(R(s)+gamma*max(sums))
            delta = np.float64(max(delta, abs(V1[s] - V[s])))


            # V1[s] = R(s) + gamma * max([sum([p * V[s1] for (s1, p) in T(s, a)]) for a in actions(s)])
            #calculate maximum difference in value
            # delta = max(delta, abs(V1[s] - V[s]))

        #check for convergence, if values converged then return V
        if delta < epsilon * (1 - gamma) / gamma:
             return V

def best_policy(V,car_index):

    states = mdp.states
    actions = mdp.actions
    pi = {}
    for s in states:
        if s!=cars_end[car_index]:
            # pi[s] = max(actions(s), key=lambda a: expected_utility(a, s, V))
            li = {}
            for a in actions( s ):
                li[a] = expected_utility( a, s, V )
            max_ele = max( li.values() )
            dir_list = []
            for key in li.keys():
                if li[key] == max_ele:
                    dir_list.append( key )
            if len( dir_list ) > 1:
                preference = ['U', 'D', 'R', 'L']
                for ele in preference:
                    if ele in dir_list:
                        pi[s] = ele
                        break
            else:
                pi[s] = dir_list[0]

        else:
            pi[s]='END'
    return pi


def expected_utility(a, s, V):
    T = mdp.T
    return np.float64(sum([np.float64(p * V[s1]) for (s1, p) in mdp.T(s, a)]))

pi_array=[]
for car_index in range(nc):
    mdp = MarkovDecisionProcess(transition=transition_array[car_index], reward=Rewards_array[car_index] )
    V=value_iteration(mdp)

    pi = best_policy(V,car_index)
    pi_array.append(pi)


def turn_left(state,move):
    i=state[0]
    j=state[1]
    ans=None
    if move=='R':
        ans=(i,max(j-1,0))
    elif move=='L':
        ans=(i,min(j+1,n-1))
    elif move=='U':
        ans=(max(i-1,0),j)
    elif move=='D':
        ans=(min(i+1,n-1),j)
    return ans

def turn_right(state,move):
    i=state[0]
    j=state[1]
    ans=None
    if move=='R':
        ans=(i,min(j+1,n-1))
    elif move=='L':
        ans=(i,max(0,j-1))
    elif move=='U':
        ans=(min(i+1,n-1),j)
    elif move=='D':
        ans=(max(i-1,0),j)
    return ans

def goto(state,dir):
    i=state[0]
    j=state[1]
    ans=None
    if dir=='L':
        ans=(max(0,i-1),j)
    elif dir=='R':
        ans=(min(i+1,n-1),j)
    elif dir=='U':
        ans=(i,max(0,j-1))
    elif dir=='D':
        ans=(i,min(j+1,n-1))
    return ans

def turn_opposite(state,dir):
    i=state[0]
    j=state[1]
    ans=None
    if dir=='L':
        ans=(min(n-1,i+1),j)
    elif dir=='R':
        ans=(max(i-1,0),j)
    elif dir=='U':
        ans=(i,min(n-1,j+1))
    elif dir=='D':
        ans=(i,max(j-1,0))
    return ans

fdo=open('output.txt','w+')
def simulation():
    answer=[]
    for i in range(nc):

        rew_global=[]
        Reward=Rewards_array[i]
        pi=pi_array[i]
        for j in range(10):
            pos=cars_start[i]
            np.random.seed(j)
            swerve=np.random.random_sample(1000000).astype(np.float64)
            k=0
            rew_local=0
            while pos!=cars_end[i]:
                dir=pi[pos]
                cur_state=pos
                res_state=pos

                if swerve[k]>0.7:
                    if swerve[k]>0.8:
                        if swerve[k]>0.9:
                            res_state=turn_opposite(cur_state,dir)
                        else:
                            res_state=turn_right(cur_state,dir)
                    else:
                        res_state=turn_left(cur_state,dir)
                else:

                    res_state=goto(pos,dir)

                k = k + 1
                pos=res_state
                rew_local=rew_local+Reward[pos]

            rew_global.append(rew_local)
        avg=sum(rew_global)//10
        # print avg
        answer.append(str(avg))
        fdo.write(str(avg))
        fdo.write('\n')

simulation()


