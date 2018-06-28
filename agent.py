from state import Cell, CellGrid2D
import random


class Agent(object):

    def __init__(self, policy, discount):
        self.policy = policy 
        self.utilities  =[(0.0, 0)] * len(self.policy)
        self.discount = discount
        self.reset()

    def reset(self):
        self.state = None
        self.action = None
        self.rewards = []

    def action(self, available_actions):
        if self.policy[0] is None:
            # Random policy
            action = random.choice(available_actions)
        else:
            action = self.policy.at(self.state)
        return action

    def utilities_string(self, indexer):
        result = ""
        for i in range(len(self.utilities)): 
            result += "{0:.2f} ".format(self.utilities[i][0])
            if (i + 1) % indexer == 0:
                result += "\n"
        return result


class DirectLearner(Agent):

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


class TemporalDifferenceLearner(Agent):

    def __init__(self, policy, discount=1.0):
        super().__init__(policy, discount)

    @staticmethod
    def learning_rate(n):
        return 60 / (59 + n)

    def update(self, s1, indexer):
        # Initialise utility of next state
        i1 = indexer * s1.x + s1.y
        u1, n1 = self.utilities[i1]
        if self.utilities[i1][0] == 0:
            self.utilities[i1] = (s1.reward, n1)
        # Update utility of present state
        if self.state is not None:
            i0 = indexer * self.state.x + self.state.y
            u0, n0 = self.utilities[i0]
            r0 = self.state.reward
            # Update utility by temporal difference (TD)
            self.utilities[i0] = (u0 + self.learning_rate(n0 + 1) * \
                    (r0 + self.discount * u1 - u0), n0 + 1)
        # Select action and update state
        self.state = s1
        if self.state.terminal:
            self.action = None
        else:
            self.action = self.policy.at(self.state)


class ADPLearner(Agent):

    def __init__(self, policy, discount=1.0):
        super().__init__(policy, discount)
        # P(t| s, a) = f(t,          s,          a)
        # self.model = {(Cell(0, 0), Cell(0, 1), Cell(0, -1)) : 0.3}
        self.utilities = {} # overrides Agent data structure
        self.rewards = {}
        self.model = {}
        self.freq_sa = {}
        self.freq_ssa = {}

    def reset(self):
        self.state = None
        self.action = None
        self.rewards = {}

    def update(self, s1, indexer):
        # Initial utilities and rewards if s1 is new
        if self.utilities.get(s1) == None:
            self.utilities[s1] = s1.reward
            self.rewards[s1] = s1.reward
        if self.state is not None:
            # Occurrences of state-action
            self.increment(self.freq_sa, (self.state, self.action))
            self.increment(self.freq_ssa, (s1, self.state, self.action))
            # Model, using relative frequency
            for ssa in self.freq_ssa.keys():
                t = ssa[0]
                if self.freq_ssa.get((t, self.state, self.action)) is None:
                    continue
                self.model[(t, self.state, self.action)] = \
                        self.freq_ssa[(t, self.state, self.action)] / \
                        self.freq_sa[(self.state, self.action)]
        # Utilities
        self.policy_evaluation()
        # Next state and action
        self.state = s1
        if self.state.terminal:
            self.action = None
        else:
            self.action = self.policy.at(self.state)

    def increment(self, d, key):
        d[key] = 1 if d.get(key) is None else d[key] + 1

    def policy_evaluation(self):
        # Uses self.[policy, utilities, model, rewards, discount]
        k = 10 # configurable
        for s in self.utilities.keys():
            for i in range(k):
                u_next = 0
                for s1, s0, a in self.freq_ssa.keys():
                    if s0 == s:
                        u_next += self.model[(s1, s0, self.policy.at(s0))] * \
                                self.utilities[s1]
                r = 0 if self.rewards.get(s) is None else self.rewards[s]
                self.utilities[s] = r + self.discount * u_next

    def utilities_string(self, indexer):
        grid = []
        for s in self.utilities.keys():
            while len(grid) <= s.x:
                grid.append([])
            while len(grid[s.x]) <= s.y:
                grid[s.x].append(0.0)
            grid[s.x][s.y] = self.utilities[s]

        result = ""
        for i in range(len(grid)): 
            for j in range(len(grid[i])):
                result += "{0:.2f} ".format(grid[i][j])
            result += "\n"
        return result
