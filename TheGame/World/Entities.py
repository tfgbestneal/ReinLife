class Empty:
    """ An empty Tile """
    def __init__(self, coordinates, value):
        self.i, self.j = coordinates
        self.value = value
        self.coordinates = list(coordinates)


class Entity:
    """ An Entity """
    def __init__(self, coordinates, value):
        self.i, self.j = coordinates
        self.value = value
        self.coordinates = list(coordinates)


class Agent:
    """ An Agent with several trackers and movement options """
    def __init__(self, coordinates, value, brain=None, gen=None, genome=None, config=None):
        self.i, self.j = coordinates
        self.health = 200
        self.value = value
        self.coordinates = list(coordinates)
        self.target_coordinates = list(coordinates)
        self.dead = False
        self.done = False
        self.age = 0
        self.max_age = 50
        self.brain = brain
        self.i_target = None
        self.j_target = None
        self.reproduced = False
        self.gen = gen
        self.fitness = 0
        self.action = -1
        self.killed = 0
        self.ate_berry = -1

        self.reward = None
        self.state = None
        self.state_prime = None
        self.info = None
        self.prob = None

        # NEAT
        self.genome = genome

        if self.genome:
            self.genome.fitness = 0
            self.config = config

    def move(self):
        self.i = self.i_target
        self.j = self.j_target
        self.coordinates = [self.i, self.j]

    def target_location(self, i, j):
        self.i_target = i
        self.j_target = j
        self.target_coordinates = [i, j]

    def learn(self, **kwargs):
        if self.brain.method == "PPO":
            self.brain.learn(age=self.age, dead=self.dead, action=self.action, state=self.state, reward=self.reward,
                             state_prime=self.state_prime, done=self.done, prob=self.prob)
        elif self.brain.method == "DRQN":
            self.brain.learn(age=self.age, dead=self.dead, action=self.action, state=self.state, reward=self.reward,
                             state_prime=self.state_prime, done=self.done, **kwargs)
        elif self.brain.method in ["DQN", "A2C", "PERDQN"]:
            self.brain.learn(age=self.age, dead=self.dead, action=self.action, state=self.state, reward=self.reward,
                             state_prime=self.state_prime, done=self.done)
        else:
            self.brain.learn(age=self.age, dead=self.dead, action=self.action, state=self.state, reward=self.reward,
                             state_prime=self.state_prime, done=self.done, **kwargs)

    def scramble_brain(self):
        if self.brain.method == "PERD3QN":
            self.brain.apply_gaussian_noise()

