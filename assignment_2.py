""""Author: Katarína Stasová
    Program uses a simple barrier to execute a part of code with all threads before the next
    part of code start to execute. """
from fei.ppds import Thread, Semaphore, Mutex, print, Event


class TurnstileBarrier:
    """"A barrier for waiting for all threads to complete the part of code. It uses turnstile.
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
        The turnstile method wait() blocks all threads and releases n threads after method signal(n)

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


def use_barrier(barrier, thread_id):
    """All threads executing this function. Each of thread print the sentence before barrier with id.
    Barrier waits for all threads. Each of thread print the sentence after barrier with id in the loop.
    -It uses event as barrier.

    :param barrier: Instance of EventBarrier
    :param thread_id: Id of thread

    :rtype: None
    """
    while True:
        print("Thread %d before barrier" % thread_id)
        barrier.wait()
        print("Thread %d after barrier" % thread_id)
        barrier.wait()


def use_two_barriers(barrier_1, barrier_2, thread_id):
    while True:
        print("Thread %d before barrier" % thread_id)
        barrier_1.wait()
        print("Thread %d after barrier" % thread_id)
        barrier_2.wait()


def first_variation(thread_count):
    """Create threads to execute program with using turnstile

    :param thread_count: the number of threads used in the program

    :rtype: None
    """
    tb_1 = TurnstileBarrier(thread_count)
    tb_2 = TurnstileBarrier(thread_count)
    threads = [Thread(use_two_barriers, tb_1, tb_2, i) for i in range(thread_count)]
    [t.join() for t in threads]


def second_variation(thread_count):
    """Create threads to execute program with using event

    :param thread_count: the number of threads used in the program

    :rtype: None
    """

    eb = EventBarrier(thread_count)
    threads = [Thread(use_barrier, eb, i) for i in range(thread_count)]
    [t.join() for t in threads]


if __name__ == '__main__':
    thread_count = 5
    first_variation(thread_count)
    # second_variation(thread_count)
