
class Agent(object):

    def __init__(self, env, policy):
        self.env = env
        self.policy = policy 
        self.state = None

    def act(self):
        pass


class PassiveGridNavigator(Agent):

    def __init__(self, env, policy):
        super().__init__(env, policy)

    def act(self):
        action = self.policy.at(self.state)
        print("Action:", action)
        self.state = self.env.transition(self.state, action)

    def done(self):
        return self.state.terminal
