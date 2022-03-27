""""Author: Katarína Stasová
    License: MIT
    Program of barber problem. One barber cuts hair of his customers. In the waiting room can be a maximum of MAX_COUNT
    customers. They live own life and when hair grows up, they visit the barber. If the waiting room is full, they will
    come later.

"""

from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, Mutex, Event, print


class EventBarrier:
    """"A reusable barrier for end of customer service. It uses event. """

    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of threads to terminate the barrier
         count - the number of waiting threads in event
         mutex - synchronization tool to make the critical area atomically executed
         event - synchronization tool to management threads
        :param thread_count: 2 (1 barber, 1 customer)
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """Waiting until barber end cutting and customer have completed styling own hair.
        Between locked mutex is code automatically executed.
        The event method wait() blocks all threads, which invoke it, until method signal() happened.
        The event method clear() activates wait(), when each thread is released from the barrier.
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()
            self.event.clear()
        last = self.count
        self.mutex.unlock()

        if last:
            self.event.wait()


class Shared:
    """Shared class for all threads."""

    def __init__(self):
        """
        customers_count = customers in the waiting room.
        queue = customers waiting for the barber in order as they arrived to the waiting room.
        customer_done = the customer signals to barber that he is satisfied and barber can end his work.
        barber_done = the barber agrees that he has completed his work.
        customer = customer signal to barber, that he is in waiting room.
        mutex - synchronization tool to make the critical area atomically executed
        """
        self.customers_count = 0
        self.queue = []
        self.customer_done = Semaphore(0)
        self.barber_done = Semaphore(1)
        self.customer = Semaphore(0)
        self.barber = Semaphore(1)
        self.mutex = Mutex()
        self.barrier = EventBarrier(2)


def haircut_done(shared, activity):
    """ Customer informs that he is satisfied with hairstyle.
        Barber informs that he finished the cutting.

    :param shared: shared class for all threads
    :param activity: information about human activity.
    :return:
    """
    print("End of " + activity + ".")
    shared.barrier.wait()


def get_hair_cut(shared):
    """Customer inform, that he sits to the barber chair.

    :param shared: shared class for all threads
    """
    print("Customer is sitting to the barber chair.")
    sleep(randint(60, 70) / 100)
    haircut_done(shared, "styling")


def live_life_and_let_hair_grow():
    """Live own life between cutting hair."""
    sleep(randint(10, 100) / 100)


def customer(shared, max_count, barber_semaphore):
    """Customers are waiting in waiting room while barber calls them to make the hairstyle to one by one.

    :param shared: shared class for all threads.
    :param max_count: max count of customers in a  waiting room.
    :param barber_semaphore: Every customer has own barber synchronization tool (Semaphore). Through this tool can
                            barber informs customer, that he can cut him.
    """
    while True:
        live_life_and_let_hair_grow()

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
    """ Barber inform, that he is ready to cut hair.

    :param shared: shared class for all threads
    """
    print("Barber is ready for cutting a customer.")
    sleep(randint(50, 60) / 100)
    haircut_done(shared, "cutting")


def barber(shared):
    """ Barber cuts customers in order as they come to the waiting room.

    :param shared: shared class for all threads
    """
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
    """Create one barber thread and C_COUNT customers."""
    MAX_COUNT = 6
    shared = Shared()
    barber = [Thread(barber, shared)]
    customers = [Thread(customer, shared, MAX_COUNT, Semaphore(0)) for _ in range(3)]

    [thread.join() for thread in barber + customers]
