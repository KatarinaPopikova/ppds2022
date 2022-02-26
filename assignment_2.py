""""Author: Katarína Stasová
    Program uses a simple barrier to execute a part of code with all threads before the next
    part of code start to execute. """
from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, print, Event


class TurnstileBarrier:
    """"A barrier for waiting for all threads to complete the part of code. It uses turnstile.
    In this implemented class are needed two instances of class for reuse barrier.
    """

    def __init__(self, thread_count):
        """Turnstile barrier initialization:
         all_thread_count - the number of threads used in the program
         count - the number of waiting threads in turnstile
         mutex - synchronization tool to make the critical area atomically executed
         turnstile - synchronization tool to management threads

        :param thread_count: the number of threads used in the program
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        """Waiting until all threads have completed part of the code.
        Between locked mutex is code automatically executed.
        The turnstile method wait() blocks all threads and releases n threads after method signal(n).

        :rtype: None
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.turnstile.signal(self.all_thread_count)
        self.mutex.unlock()
        self.turnstile.wait()


class EventBarrier:
    """"A barrier for waiting for all threads to complete the part of code. It uses event.
    This barrier is simple reusable.
    """

    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of threads used in the program
         count - the number of waiting threads in event
         mutex - synchronization tool to make the critical area atomically executed
         event - synchronization tool to management threads

        :param thread_count: the number of threads used in the program
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """Waiting until all threads have completed part of the code.
        Between locked mutex is code automatically executed.
        The event method wait() blocks all threads, which invoke it, until method signal() happened.
        The event method clear() activates wait().

        :rtype: None
        """
        self.mutex.lock()
        if self.count == 0:
            self.event.clear()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()


class EventBarrier2:
    """"A barrier for waiting for all threads to complete the part of code. It uses event.
    In this implemented class are needed two instances of class for reuse barrier.
    """

    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of threads used in the program
         count - the number of waiting threads in event
         mutex - synchronization tool to make the critical area atomically executed
         event - synchronization tool to management threads

        :param thread_count: the number of threads used in the program
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """Waiting until all threads have completed part of the code.
        Between locked mutex is code automatically executed.
        The event method wait() blocks all threads, which invoke it, until method signal() happened.
        The event method clear() activates wait(), when each thread is released from the barrier.

        :rtype: None
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.event.signal()
        self.mutex.unlock()
        self.event.wait()

        self.mutex.lock()
        self.count -= 1
        if self.count == 0:
            self.event.clear()
        self.mutex.unlock()


def rendezvous(thread_name):
    """ Every threads print 'rendezvous' competitive with their name (with id)
        The print() method from fei.ppds is run synchronously

    :param thread_name: Name of thread with id

    :rtype: None
    """
    sleep(randint(1, 10) / 10)
    print('rendezvous: %s' % thread_name)


def ko(thread_name):
    """ Every threads print 'ko' competitive with their name (with id)
        The print() method from fei.ppds is run synchronously

    :param thread_name: Name of thread with id

    :rtype: None
    """
    print('ko: %s' % thread_name)
    sleep(randint(1, 10) / 10)


def use_barrier(barrier, thread_name):
    """All threads executing this function. Each of thread print the sentence before barrier with id.
    Barrier waits for all threads. Each of thread print the sentence after barrier with id.
    Barrier again waits for all threads. This is executed in the cycle.
    -It uses event as barrier.

    :param barrier: Instance of EventBarrier
    :param thread_name: Name of thread with id

    :rtype: None
    """
    while True:
        rendezvous(thread_name)
        barrier.wait()
        ko(thread_name)
        barrier.wait()


def use_two_barriers(barrier_1, barrier_2, thread_name):
    """All threads executing this function. Each of thread print the sentence before first barrier with id.
    First barrier waits for all threads. Each of thread print the sentence after barrier with id.
    Second barrier waits for all threads. This is executed in the cycle.
    -If barrier_1 and barrier_2 are instance of TurnstileBarrier, it uses turnstile as barrier.
    -If barrier_1 and barrier_2 are instance of EventBarrier2, it uses event as barrier.

    :param barrier_1: Instance of TurnstileBarrier or EventBarrier2
    :param barrier_2: Instance of TurnstileBarrier or EventBarrier2
    :param thread_name: Name of thread with id

    :rtype: None
    """
    while True:
        rendezvous(thread_name)
        barrier_1.wait()
        ko(thread_name)
        barrier_2.wait()


def first_variation(thread_count):
    """Create threads to execute program with using turnstile

    :param thread_count: the number of threads used in the program

    :rtype: None
    """
    tb_1 = TurnstileBarrier(thread_count)
    tb_2 = TurnstileBarrier(thread_count)
    threads = [Thread(use_two_barriers, tb_1, tb_2, 'Thread %d' % i) for i in range(thread_count)]
    [t.join() for t in threads]


def second_variation(thread_count):
    """Create threads to execute program with using event

    :param thread_count: the number of threads used in the program

    :rtype: None
    """

    eb = EventBarrier(thread_count)
    threads = [Thread(use_barrier, eb, 'Thread %d' % i) for i in range(thread_count)]
    [t.join() for t in threads]


def third_variation(thread_count):
    """Create threads to execute program with using event

    :param thread_count: the number of threads used in the program

    :rtype: None
    """

    eb_1 = EventBarrier2(thread_count)
    eb_2 = EventBarrier2(thread_count)
    threads = [Thread(use_two_barriers, eb_1, eb_2, 'Thread %d' % i) for i in range(thread_count)]
    [t.join() for t in threads]


if __name__ == '__main__':
    thread_count = 5
    # first_variation(thread_count)
    # second_variation(thread_count)
    third_variation(thread_count)
