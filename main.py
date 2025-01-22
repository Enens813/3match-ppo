from environment import Match3BluestacksEnv
from ppo import PPOAgent, PPOMemory


def train_match3_agent(num_episodes=1000, max_timesteps=200, update_timestep=2000):
    """
    :param num_episodes: how many episodes (rounds/games) to run
    :param max_timesteps: max steps per episode
    :param update_timestep: how many timesteps to collect before we run an update
    """
    env = Match3BluestacksEnv()
    agent = PPOAgent(state_shape=(8,8), action_dim=env.action_space.n, lr=1e-3, gamma=0.99, eps_clip=0.2, K_epochs=4)
    memory = PPOMemory()

    timestep = 0
    for episode in range(num_episodes):
        state = env.reset()
        for t in range(max_timesteps):
            timestep += 1
            
            # 1) Select action
            action, logprob, value = agent.select_action(state)
            
            # 2) Environment step
            next_state, reward, done, info = env.step(action)
            
            # 3) Store transition in memory
            memory.store(state, action, logprob, reward, done, value)
            
            # 4) Update state
            state = next_state

            # If we've gathered enough steps, do a PPO update
            if timestep % update_timestep == 0:
                agent.update(memory)
                memory.clear()

            if done:
                print(f"Episode {episode} finished after {t+1} timesteps.")
                break
