
import time
from robertcommon.system.driver.agent import Agent
from robertcommon.basic.cls.utils import daemon_thread

class Agent1(Agent):


    def run_once(self):
        while True:
            print(f"Agent1: {time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))}\n")
            time.sleep(1)


class Agent2(Agent):


    def run_once(self):
        while True:
            print(f'Agent2: {time.time()}\n')
            time.sleep(1)

a1 = Agent1()
a2 = Agent2()
agents = [a1, a2]
for agent in agents:
    agent.run().start()

input()
