import worlds
import agents
import time

def main():
    env = worlds.World()
    agent = agents.DeceptiveAgent()
    actions = agent.findPath(env)
    time.sleep(1)
    for action in actions:
        env.agent_step(action)

if __name__ == '__main__':
    main()
