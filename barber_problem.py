from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, Mutex


class Shared:
    def __init__(self):
        self.customers_count = 0
        self.queue = []
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(1)
        self.customer = Semaphore(0)
        self.barber = Semaphore(1)
        self.mutex = Mutex()


def get_hair_cut(shared):
    sleep(randint(60, 70) / 100)


def customer(shared, max_count, barber_semaphore):
    while True:

        shared.mutex.lock()
        if shared.customers_count == max_count:
            return

        shared.customers_count += 1
        shared.queue.append(barber_semaphore)
        shared.mutex.unlock()
        shared.customer.signal()
        barber_semaphore.wait()

        get_hair_cut(shared)

        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.customers_count -= 1
        shared.mutex.unlock()


def cut_hair(shared):
    sleep(randint(50, 60) / 100)


def barber(shared):
    while True:
        shared.customer.wait()
        shared.mutex.lock()
        active_barber = shared.queue.pop()
        shared.mutex.unlock()
        active_barber.signal()

        cut_hair(shared)

        shared.customer_done.wait()
        shared.barber_done.signal()


if __name__ == '__main__':
    MAX_COUNT = 6
    shared = Shared()
    barber = [Thread(barber, shared)]
    customers = [Thread(customer, shared, MAX_COUNT, Semaphore(0)) for _ in range(3)]

    [thread.join() for thread in barber + customers]
