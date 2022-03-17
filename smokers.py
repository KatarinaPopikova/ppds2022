""""Author: Katarína Stasová
    License: MIT
    Program for simulation in warehouse. Producers produce and add items to warehouse and consumers gaining
    them and producing. """

from fei.ppds import Thread


class Shared:
    def __init__(self):
        pass


def make_cigarette(name):
    pass


def smoke(name):
    pass


def agent_1(shared):
    while True:
        pass


def agent_2(shared):
    while True:
        pass


def agent_3(shared):
    while True:
        pass


def smoker_paper():
    while True:
        pass


def smoker_tobacco():
    while True:
        pass


def smoker_match():
    while True:
        pass


def pusher_paper():
    while True:
        pass


def pusher_tobacco():
    while True:
        pass


def pusher_match():
    while True:
        pass


if __name__ == '__main__':
    shared = Shared()
    smokers = []
    smokers.append(Thread(smoker_match, shared))
    smokers.append(Thread(smoker_tobacco, shared))
    smokers.append(Thread(smoker_paper, shared))

    agents = []
    agents.append(Thread(agent_1, shared))
    agents.append(Thread(agent_2, shared))
    agents.append(Thread(agent_3, shared))

    [t.join() for t in smokers + agents]
