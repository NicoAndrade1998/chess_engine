from chess_env import ChessEnv
from ppo_agent import PPOAgent

env = ChessEnv()
agent = PPOAgent()

episodes = 100

for ep in range(episodes):

    state = env.reset()
    done = False
    total_reward = 0

    while not done:

        action, log_prob, value = agent.select_action(state, env)

        decoded_action = action  # already encoded index

        # convert back
        from utils import decode_move
        move = decode_move(decoded_action)

        next_state, reward, done = env.step(move)

        agent.store((state, action, reward, log_prob, value))

        state = next_state
        total_reward += reward

    agent.update()

    print(f"Episode {ep}: reward {total_reward}")