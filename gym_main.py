# Create the environment
from gym_3match import ThreeMatchGameEnv

env = ThreeMatchGameEnv()

# Reset the environment
state = env.reset()

# Run the game for 10 steps (for example)
for _ in range(10):
    env.render()
    # Random action (just as an example)
    action = env.action_space.sample()  
    state, reward, done, info = env.step(action)
    
    if done:
        print("Game over!")
        break

env.close()
