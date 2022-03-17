""""Author: Katarína Stasová
    License: MIT
    Program of savage problem. When agents have an infinite amount of materials, and 3 smokers each have an infinite
     amount of one different material."""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Semaphore, print

N = 10
M = 3
S = 5


class Shared:
    def __init__(self, m, s):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)


def savage(i, shared, s):
    sleep(randint(1, 100) / 100)
    while True:

        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: empty pot')
            shared.empty_pot.signal(s)
            shared.full_pot.wait()

        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def eat(i):
    sleep(randint(50, 200) / 100)


def cook(cooker_id, shared, m):
    while True:

        shared.empty_pot.wait()
        print(f'cooker {cooker_id}: cooking')
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
