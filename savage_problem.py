""""Author: Katarína Stasová
    License: MIT
    Program of savage problem. Savages eat from pot and when pot is empty, savage wakes up the chefs. They cook and
    serve to pot. When pot is full, savages can continue to eat."""

from random import randint
from time import sleep
from fei.ppds import Thread, Mutex, Event, Semaphore, print

N = 10
M = 3
S = 5


class EventBarrier:
    """"A reusable barrier for waiting for all sensors to complete the part of code. It uses event. """

    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of sensors
         count - the number of waiting threads in event
         mutex - synchronization tool to make the critical area atomically executed
         event - synchronization tool to management threads
        :param thread_count: the number of sensors
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self, shared, servings_count):
        """Waiting until all sensors have completed part of the code.
        Between locked mutex is code automatically executed.
        The event method wait() blocks all threads, which invoke it, until method signal() happened.
        The event method clear() activates wait(), when each thread is released from the barrier.
        When count is full, that is, the chefs cooked m servings and filled the bowl. Savages can eat.
        :param shared: shared class for all threads
        :param servings_count: required number of servings
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            shared.servings += servings_count
            shared.full_pot.signal()
            self.count = 0
            self.event.signal()
            self.event.clear()
        last = self.count
        self.mutex.unlock()

        if last:
            self.event.wait()


class Shared:
    """
    Shared class for all threads.
    """

    def __init__(self, servings_count, chefs_count):
        """
        servings- the current number of servings in the pot
        mutex - synchronization tool to make the critical area atomically executed
        empty_pot- signals an empty pot
        full_pot- signals an full pot
        barrier- wait for all chefs

        :param servings_count: required number of servings
        :param chefs_count: the number of chefs
        """
        self.servings = servings_count
        self.mutex = Mutex()
        self.empty_pot = Semaphore(0)
        self.full_pot = Semaphore(0)
        self.barrier = EventBarrier(chefs_count)


def eat(savage_id):
    """ Simulation of eating.

    :param savage_id: savage id
    """
    print(f'savage {savage_id}:eat start')
    sleep(randint(50, 200) / 100)
    print(f'savage {savage_id}:eat end')


def savage(savage_id, shared, chefs_count):
    """ Simulation of savages eating. Savage who find out, that the pot is empty wake up chefs. He is waiting until the
    pot is full.

    :param savage_id: savage id
    :param shared: shared class for all threads
    :param chefs_count: the number of chefs
    """
    while True:
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {savage_id}: empty pot')
            shared.empty_pot.signal(chefs_count)
            shared.full_pot.wait()

        print(f'savage {savage_id}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat(savage_id)


def cooking(chef_id, servings_count):
    print(f'chef {chef_id}: cooking')
    sleep(randint(1, 4) / 10)
    print(f'chef {chef_id}: cook {servings_count} servings --> pot')


def chef(chef_id, shared, servings_count):
    """ Simulation of chefs cooking. When pot is empty, they wake up and start cooking together. The last chef serves
    servings to the pot and savages can continue in eating.

    :param chef_id: chef id
    :param shared: shared class for all threads
    :param servings_count: required number of servings
    """
    while True:
        shared.empty_pot.wait()
        cooking(chef_id, servings_count)
        shared.barrier.wait(shared, servings_count)


if __name__ == '__main__':
    """Create threads."""
    shared = Shared(0, S)
    threads = list()

    for savage_id in range(N):
        t = Thread(savage, savage_id, shared, S)
        threads.append(t)

    for chef_id in range(S):
        t = Thread(chef, chef_id, shared, M)
        threads.append(t)

    for t in threads:
        t.join()
