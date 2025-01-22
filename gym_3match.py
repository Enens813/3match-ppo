import gym
from gym import spaces
import numpy as np

class ThreeMatchGameEnv(gym.Env):
    def __init__(self):
        super(ThreeMatchGameEnv, self).__init__()
        
        # Initialize the game state (3 matchsticks to start)
        self.initial_matchsticks = 3
        self.reset()

        # Action space: 1 or 2 matchsticks to remove
        self.action_space = spaces.Discrete(2)  # action 0 -> take 1 matchstick, action 1 -> take 2 matchsticks

        # Observation space: number of matchsticks remaining
        self.observation_space = spaces.Discrete(self.initial_matchsticks + 1)  # 0 to 3 matchsticks

    def reset(self):
        # Reset the game state, set matchsticks to initial count
        self.matchsticks = self.initial_matchsticks
        return self.matchsticks  # return the initial state (number of matchsticks)

    def step(self, action):
        if action == 0:
            self.matchsticks -= 1  # Take 1 matchstick
        elif action == 1:
            self.matchsticks -= 2  # Take 2 matchsticks

        # Ensure the number of matchsticks is non-negative
        self.matchsticks = max(self.matchsticks, 0)

        # Check if the game is over
        done = False
        if self.matchsticks == 0:
            done = True  # Game ends when there are no matchsticks left
        
        # Reward structure: Avoid losing the game
        if self.matchsticks == 0:
            reward = -10  # Penalty for losing (taking the last matchstick)
        else:
            reward = 1  # Reward for avoiding the last matchstick

        # Return state, reward, done (whether the game is over), and info (optional)
        return self.matchsticks, reward, done, {}

    def render(self):
        # Display the current number of matchsticks
        print(f"Matchsticks remaining: {self.matchsticks}")

    def close(self):
        pass
