""""Author: Katarína Stasová
    Program for simulation in warehouse. Producers produce and add items to warehouse and consumers gaining
    them and producing. """
from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, print


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


def producer(shared):
    """ Simulation of warehouse by the producer.
    Produce products and storage products when no consumer is in a warehouse.

    :param shared:
    """
    while True:
        # production
        sleep(randint(1, 10) / 10)
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        # storage of the product in the warehouse
        sleep(randint(1, 10) / 100)
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
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        shared.free.signal()
        # product processing
        sleep(randint(1, 10) / 10)


if __name__ == '__main__':
    """ Create threads for consumers and producers."""
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
