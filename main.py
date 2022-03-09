from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print


class LS(object):
    def __init__(self):
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        self.mutex.lock()
        if not self.cnt:
            sem.wait()
        self.cnt += 1
        self.mutex.unlock()

    def unlock(self, sem):
        self.mutex.lock()
        self.cnt -= 1
        if not self.cnt:
            sem.signal()
        self.mutex.unlock()


class Shared(object):
    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)


def producer(shared):
    while True:
        # production
        sleep(randint(1, 10) / 10)
        # warehouse vacancy check
        shared.free.wait()
        if shared.finished:
            break
        # gaining access to the warehouse
        shared.mutex.lock()
        # storage of the product in the warehouse
        sleep(randint(1, 10) / 100)
        # leaving the warehouse
        shared.mutex.unlock()
        # increase in the number of stocks in the warehouse
        shared.items.signal()


def consumer(shared):
    while True:
        # checking the number of stocks in the warehouse
        shared.items.wait()
        if shared.finished:
            break
        # gaining access to the warehouse
        shared.mutex.lock()
        # gaining the product from the warehouse
        sleep(randint(1, 10) / 100)
        # leaving the warehouse
        shared.mutex.unlock()
        # product processing
        sleep(randint(1, 10) / 10)


if __name__ == '__main__':
    for i in range(10):
        s = Shared(10)
        c = [Thread(consumer, s) for _ in range(2)]
        p = [Thread(producer, s) for _ in range(5)]

        sleep(10)
        s.finished = True
        print(f"The main thread {i}: is waiting to be completed")
        s.items.signal(100)
        s.free.signal(100)
        [t.join() for t in c + p]
        print(f"The main thread {i}: end of program")
