""""Author: Katarína Stasová
    License: MIT
    Program of savage problem. Savages eat from pot and when pot is empty, savage wakes up the cooks. They cook and
    serve to pot. When pot is full, savages can continue to eat."""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Event, Semaphore, print

N = 10
M = 3
S = 5


class EventBarrier:
    def __init__(self, thread_count):
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self, m):
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            shared.servings += m
            shared.full_pot.signal()
            self.count = 0
            self.event.signal()
            self.event.clear()
        last = self.count
        self.mutex.unlock()

        if last:
            self.event.wait()


class Shared:
    def __init__(self, m, s):
        self.servings = m
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier = EventBarrier(s)


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
    print(f'savage {i}:eat start')
    sleep(randint(50, 200) / 100)
    print(f'savage {i}:eat end')


def cook(cooker_id, shared, m):
    while True:
        shared.empty_pot.wait()
        print(f'cooker {cooker_id}: cooking')
        sleep(randint(1, 4) / 10)
        print(f'cooker {cooker_id}: cook {m} servings --> pot')
        shared.barrier()


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
