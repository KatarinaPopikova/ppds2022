""""Author: Katarína Stasová
    Program for simulation in warehouse. Producers produce and add items to warehouse and consumers gaining
    them and producing. """
from random import randint
from time import sleep

import numpy
from fei.ppds import Thread, Semaphore, Mutex
from matplotlib import pyplot as plt, cm, print


class Shared(object):
    """Shared class for all threads"""

    def __init__(self, thread_count):
        """initialization of:
        -simulation finishing = finished
        -synchronization object to maintain data integrity = mutex
        -free space in the warehouse as free
        -empty warehouse as items (semaphore set to 0)

        :param thread_count: count of threads
        """
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(thread_count)
        self.items = Semaphore(0)
        self.produced_items = 0


def producer(shared, prod_time):
    """ Simulation of warehouse by the producer.
    Produce products and storage products when no consumer is in a warehouse.

    :param shared:
    """
    while True:
        # production
        sleep(prod_time)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.produced_items += 1
        # storage of the product in the warehouse
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    """ Simulation of warehouse by the consumer.
    Gaining products when no producer is in a warehouse.

    :param shared:
    """
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # gaining the product from the warehouse
        sleep(randint(1, 10) / 1000)
        shared.mutex.unlock()
        shared.free.signal()
        # product processing
        sleep(randint(1, 10) / 100)


if __name__ == '__main__':
    """ Create threads for consumers and producers.
    """
    produced_items = []
    production_time = list(map(lambda x: x / 500, range(10, 0, -1)))
    producers = list(range(5, 15))

    for time in production_time:
        produced_items.append([])
        for prod in producers:
            produced_items_sum = 0
            for j in range(10):
                s = Shared(5)
                c = [Thread(consumer, s) for _ in range(2)]
                p = [Thread(producer, s, time) for _ in range(prod)]

                sleep(1)
                s.finished = True

                # let all threads know about the end
                s.items.signal(100)
                s.free.signal(100)
                [t.join() for t in c + p]

                produced_items_sum += s.produced_items
            produced_items[-1].append(produced_items_sum / 10)

