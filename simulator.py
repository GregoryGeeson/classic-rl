import time


class Simulator(object):

    def __init__(self, env, agent, do_print=False):
        self.env = env
        self.agent = agent
        self.rep = None
        self.indexer = 0
        self.do_print = do_print

    def run(self, episodes=100, pause=0.0, max_moves=100):
        for i in range(episodes):
            print("-- Episode {} --\n".format(i + 1))
            self.episode(pause, max_moves)
            self.agent.update_utilities(i+1, self.indexer)

    def episode(self, pause, max_moves):
        self.agent.reset(self.env.model.random())
        self.printout(pause)

        count = 0
        while not self.agent.done() and count < max_moves:
            self.agent.update_rewards()
            action = self.agent.action(
                        self.env.available_actions(self.agent.state))
            self.agent.set_state(self.env.transition(
                    self.agent.state, action))
            count += 1
            self.printout(pause, action)

        self.agent.update_rewards()


    def printout(self, pause, action=None):
        if not self.do_print:
            return
        print("s =", self.agent.state)
        if action is not None:
            print("a =", action)
        print(self)
        if pause > 0:
            time.sleep(pause)


class GridWorldSimulator(Simulator):

    def __init__(self, env, agent):
        super().__init__(env, agent)
        self.rep = self.env.model
        self.indexer = self.rep.pmax.x

    def __repr__(self):
        result = ""
        for i in range(len(self.rep)):
            state = self.rep.at_index(i)
            if self.agent.state == state:
                result += "@ "
            elif state.terminal:
                result += "x "
            elif state.accessible:
                result += "o "
            else:
                result += "# "
            if (i + 1) % self.rep.pmax.x == 0:
                result += "\n"
        return result
