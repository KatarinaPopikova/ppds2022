""""Author: Katarína Stasová
    License: MIT
    Program of barber problem. One barber cuts hair of his customers. In the waiting room can be a maximum of MAX_COUNT
    customers. They live own life and when hair grows up, they visit the barber. If the waiting room is full, they will
    come later.

"""

from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, Mutex, print


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
        self.mutex = Mutex()


def get_hair_cut():
    """Customer inform, when he sits to the barber chair and when he is satisfied with hairstyle."""
    print("Customer is sitting to the barber chair.")
    sleep(randint(30, 40) / 100)
    print("I am satisfied with this hairstyle")


def live_life_and_let_hair_grow():
    """Live own life between cutting hair."""
    sleep(randint(600, 1500) / 100)


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

        get_hair_cut()

        shared.customer_done.signal()
        shared.barber_done.wait()

        shared.mutex.lock()
        shared.customers_count -= 1
        shared.mutex.unlock()


def cut_hair():
    """ Barber inform, when he is ready to cut hair and when he finished the cutting."""
    print("Barber is ready for cutting a customer.")
    sleep(randint(40, 50) / 100)
    print("I finished the hairstyle.")


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

        cut_hair()

        shared.customer_done.wait()
        shared.barber_done.signal()


if __name__ == '__main__':
    """Create one barber thread and C_COUNT customers."""
    MAX_COUNT = 6
    CUSTOMERS_COUNT = 3
    shared = Shared()
    barber = [Thread(barber, shared)]
    customers = [Thread(customer, shared, MAX_COUNT, Semaphore(0)) for _ in range(CUSTOMERS_COUNT)]

    [thread.join() for thread in barber + customers]
