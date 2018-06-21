from state import Cell, CellGrid2D
import random


class Agent(object):

    def __init__(self, policy):
        self.policy = policy 
        self.utilities = self.init_values()
        self.discount = 1.0
        self.state = None
        self.rewards = []

    def init_values(self):
        return [0.0] * len(self.policy)

    def reset(self, s):
        self.state = s
        self.rewards = []

    def action(self, available_actions):
        if self.policy[0] is None:
            # Random policy
            action = random.choice(available_actions)
        else:
            action = self.policy.at(self.state)
        return action

    def set_state(self, s):
        self.state = s


    def done(self):
        return self.state.terminal


class PassiveGridNavigator(Agent):

    def __init__(self, policy):
        super().__init__(policy)
        self.discount = 1.0

    def init_values(self):
        return [(0.0, 0)] * len(self.policy) # (value, no. samples)

    def update_rewards(self):
        self.rewards.append((self.state, self.state.reward))

    def update_utilities(self, n, indexer):
        print("Reward sequence:", self.rewards)
        for i in range(len(self.rewards)):
            s0, r0 = self.rewards[i]
            s = indexer * s0.x + s0.y # 1D index for 2D grid
            u, n = self.utilities[s] # old value and no. samples
            # Accumulate reward-to-go
            total_reward = 0
            for j in range(i, len(self.rewards)):
                s1, r1 = self.rewards[j]
                total_reward += self.discount**(j-i) * r1
            # Take new average and increment no. samples
            self.utilities[s] = ((u * n + total_reward) / (n + 1), n + 1)

        print("Utility estimate:")
        print(self.utilities_string(indexer))

    def utilities_string(self, indexer):
        result = ""
        for i in range(len(self.utilities)): 
            result += "{0:.2f} ".format(self.utilities[i][0])
            if (i + 1) % indexer == 0:
                result += "\n"
        return result
