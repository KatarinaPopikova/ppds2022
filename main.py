""""Author: Katarína Stasová
    License: MIT
    Program for simulation in warehouse. Producers produce and add items to warehouse and consumers gaining
    them and producing. """
from random import randint
from time import sleep

import numpy
from fei.ppds import Thread, Semaphore, Mutex
from matplotlib import pyplot as plt, cm


class Shared(object):
    """Shared class for all threads"""

    def __init__(self, thread_count):
        """initialization of:
        -simulation finishing = finished
        -synchronization object to maintain data integrity = mutex
        -free space in the warehouse as free
        -empty warehouse as items (semaphore set to 0)
        -produced_items in one cycle

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

    :param prod_time: duration of one item production
    :param shared: shared class for all threads
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

    :param shared: shared class for all threads
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


def create_graph(production_time, producers, produced_items):
    """ Create 3D graph

    :param production_time: count of durations of one item production in each cycle
    :param producers: count of producers in each cycle
    :param produced_items: average of produced items
    """
    fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

    x, y = numpy.meshgrid(production_time, producers)
    z = numpy.array(produced_items)
    ax.plot_surface(x, y, z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    ax.set_xlabel("production time")
    ax.set_ylabel("producers")
    ax.set_zlabel("produced items")

    plt.show()


if __name__ == '__main__':
    """ Create list of times for production of 10 values.
    Create list of count of producers of 10 values.
    Combine them in 10 replicates and find the average.
    Create threads as consumers and producers.
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

    create_graph(production_time, producers, produced_items)
