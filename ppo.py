import torch
import torch.nn as nn
import torch.nn.functional as F

"""
Actor network: outputs a probability distribution over possible actions.
Critic network: estimates the value (expected return) of a given state.
Memory (Buffer): accumulates transitions (states, actions, rewards, etc.) for a number of steps before performing an update.
Update step: uses the collected transitions to optimize both actor and critic using PPO objectives (the clipped surrogate objective).
"""


class ActorCritic(nn.Module):
    def __init__(self, state_shape, action_dim):
        super(ActorCritic, self).__init__()
        
        # state_shape might be (8,8) from the environment
        self.state_dim = state_shape[0] * state_shape[1]
        self.action_dim = action_dim

        # Common feature extractor
        self.common = nn.Sequential(
            nn.Linear(self.state_dim, 128),
            nn.ReLU(),
            nn.Linear(128, 128),
            nn.ReLU()
        )

        # Actor head (policy)
        self.actor = nn.Linear(128, action_dim)
        
        # Critic head (value function)
        self.critic = nn.Linear(128, 1)

    def forward(self, x):
        """
        Forward pass - returns (policy_logits, value)
        x is expected to be a batch of states: shape [batch_size, state_dim]
        """
        x = self.common(x)
        policy_logits = self.actor(x)
        value = self.critic(x)
        return policy_logits, value


"""
We need a place to store state, action, log_prob, reward, etc. for each timestep, until we do an update.
"""
class PPOMemory:
    def __init__(self):
        self.states = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.dones = []
        self.values = []

    def store(self, state, action, logprob, reward, done, value):
        self.states.append(state)
        self.actions.append(action)
        self.logprobs.append(logprob)
        self.rewards.append(reward)
        self.dones.append(done)
        self.values.append(value)

    def clear(self):
        self.states = []
        self.actions = []
        self.logprobs = []
        self.rewards = []
        self.dones = []
        self.values = []


"""
The ActorCritic network and an optimizer.
A method to pick an action given the state (for exploration).
A method to update the network after collecting a batch of experiences.
"""
class PPOAgent:
    def __init__(self, state_shape, action_dim, lr=1e-3, gamma=0.99, eps_clip=0.2, K_epochs=4):
        """
        :param state_shape: shape of the state (e.g., [8,8])
        :param action_dim: number of actions (e.g., 8*8*4 = 256)
        :param lr: learning rate
        :param gamma: discount factor
        :param eps_clip: PPO clipping parameter
        :param K_epochs: number of epochs per update
        """
        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs
        
        self.policy = ActorCritic(state_shape, action_dim)
        self.optimizer = torch.optim.Adam(self.policy.parameters(), lr=lr)
        
        # Old policy for computing ratio
        self.old_policy = ActorCritic(state_shape, action_dim)
        self.old_policy.load_state_dict(self.policy.state_dict())
        
        self.MseLoss = nn.MSELoss()

    def select_action(self, state):
        """
        Given a single state, return an action, the log probability, and the value.
        state shape is (grid_size, grid_size).
        We'll flatten it to 1D for the network.
        """
        state_t = torch.FloatTensor(state.flatten()).unsqueeze(0)  # shape [1, state_dim]
        policy_logits, value = self.policy(state_t)
        
        # Categorical distribution for discrete actions
        dist = torch.distributions.Categorical(logits=policy_logits)
        action = dist.sample()
        logprob = dist.log_prob(action)
        
        return action.item(), logprob.item(), value.item()

    def update(self, memory):
        """
        Perform a PPO update using the experiences in memory.
        """
        # Convert lists to tensors
        old_states = torch.FloatTensor([s.flatten() for s in memory.states])
        old_actions = torch.LongTensor(memory.actions)
        old_logprobs = torch.FloatTensor(memory.logprobs)
        old_values = torch.FloatTensor(memory.values)

        # Compute discounted rewards-to-go
        rewards = []
        discounted_reward = 0
        for reward, is_done in zip(reversed(memory.rewards), reversed(memory.dones)):
            if is_done:
                discounted_reward = 0
            discounted_reward = reward + self.gamma * discounted_reward
            rewards.insert(0, discounted_reward)
        rewards = torch.FloatTensor(rewards)

        # Normalize the rewards if desired
        # rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-5)

        # Optimization epochs
        for _ in range(self.K_epochs):
            # Evaluate current policy
            logits, state_values = self.policy(old_states)
            dist = torch.distributions.Categorical(logits=logits)
            
            # Compute log probs w.r.t current policy
            logprobs = dist.log_prob(old_actions)
            dist_entropy = dist.entropy()

            # Ratios for PPO
            ratios = torch.exp(logprobs - old_logprobs)

            # Advantage
            advantages = rewards - state_values.squeeze().detach()

            # PPO objective
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip, 1 + self.eps_clip) * advantages
            
            # Critic loss
            critic_loss = self.MseLoss(state_values.squeeze(), rewards)
            
            # Combined loss
            loss = -torch.min(surr1, surr2).mean() + 0.5 * critic_loss - 0.01 * dist_entropy.mean()

            # Take gradient step
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()

        # Update old policy
        self.old_policy.load_state_dict(self.policy.state_dict())
