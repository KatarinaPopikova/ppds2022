from random import randint
from time import sleep
from fei.ppds import Thread

N = 10
M = 3
S = 5


class Shared:
    def __init__(self, m, s):
        pass


def savage(i, shared, s):
    sleep(randint(1, 100) / 100)
    while True:
        eat(i)


def eat(i):
    sleep(randint(50, 200) / 100)


def cook(cooker_id, shared, m):
    while True:
        sleep(randint(1, 4) / 10)


if __name__ == '__main__':
    shared = Shared(0, S)
    threads = list()

    for savage_id in range(N):
        t = Thread(savage, savage_id, shared, S)
        threads.append(t)

    for cooker_id in range(S):
        t = Thread(cook, cooker_id, shared, M)
        threads.append(t)

    for t in threads:
        t.join()
