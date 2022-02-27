""""Author: Katarína Stasová
    Program uses synchronization objects to compute fibonacci with more threads. """
from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, Event


class FibonacciIndex:
    """" Shared class for all threads. It saves the value,
    which is looking for compute fibonacci sequence.
    """

    def __init__(self):
        self.index = 0

    def get_index(self):
        """ Return actual value of index.

        :rtype: index value of instance
        """
        return self.index

    def set_index(self):
        """ Increase actual index

        :rtype: None
        """
        self.index += 1


class TurnstileBarrier:
    """"A barrier that waiting for all threads to complete the part of code. It uses turnstile.
    In this implemented class are needed two instances of class for reuse barrier.
    """

    def __init__(self, thread_count):
        """Turnstile barrier initialization:
         all_thread_count - the number of using threads
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
        The turnstile method wait() blocks all threads and releases n threads after method
        signal(n) from check_signal() is called.

        :rtype: None
        """
        self.mutex.lock()
        self.count += 1
        self.check_signal()
        self.mutex.unlock()
        self.turnstile.wait()

    def get_all_thread_count(self):
        """Return the value of all_thread_count

        :rtype: count of threads, that not executed fibonacci counting.
        """
        return self.all_thread_count

    def set_all_thread_count(self):
        """Decreasing count of threads value, because some thread executed fibonacci counting and is no longer needed.

        :rtype: None
        """
        self.all_thread_count -= 1
        self.check_signal()

    def check_signal(self):
        """Check if all necessary threads have invoked the function.

        :rtype: None
        """
        if self.count == self.all_thread_count:
            self.count = 0
            self.turnstile.signal(self.all_thread_count)


class EventBarrier:
    """"A barrier that waiting for all threads to complete the part of code. It uses event.
    In this implemented class are needed two instances of class for reuse barrier.
    """

    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of using threads
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
        if self.count == 0:
            self.event.clear()
        self.count += 1
        self.check_signal()
        self.mutex.unlock()
        self.event.wait()

    def get_all_thread_count(self):
        """Return the value of all_thread_count

        :rtype: count of threads, that not executed fibonacci counting.
        """
        return self.all_thread_count

    def set_all_thread_count(self):
        """Decreasing count of threads value, because some thread executed fibonacci counting and is no longer needed.

        :rtype: None
        """
        self.all_thread_count -= 1
        self.check_signal()

    def check_signal(self):
        """Check if all necessary threads have invoked the function.

        :rtype: None
        """
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()


def compute_fibonacci(barrier1, barrier2, fib_seq, i):
    """ Compute fibonacci using barriers (event/turnstile) as synchronization object. In the loop is looking for the
    right thread, which can continue to fill the array for the Fibonacci sequence.

    :param barrier1: instance of TurnstileBarrier/EventBarrier
    :param barrier1: instance of TurnstileBarrier/EventBarrier
    :param fib_seq: array for fibonacci sequence
    :param i: the id of thread

    :rtype: None
    """
    mutex = Mutex()
    while True:
        sleep(randint(1, 10) / 10)
        barrier1.wait()
        mutex.lock()

        if i == len(fib_seq) - barrier1.get_all_thread_count() - 2:
            break
        else:
            mutex.unlock()
            barrier2.wait()

    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]

    barrier1.set_all_thread_count()
    barrier2.set_all_thread_count()
    mutex.unlock()


def compute_fibonacci_without_barrier(f_i, fib_seq, i):
    """ Compute fibonacci using mutex as synchronization object. In the loop is looking for the right thread, which can
    continue to fill the array for the Fibonacci sequence.

    :param f_i: instance of FibonacciIndex
    :param fib_seq: array for fibonacci sequence
    :param i: the id of thread

    :rtype: None
    """
    sleep(randint(1, 10) / 10)
    mutex = Mutex()
    while True:
        mutex.lock()
        sleep(randint(1, 10) / 10)
        if f_i.get_index() == i:
            f_i.set_index()
            break
        mutex.unlock()

    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]
    mutex.unlock()


def first_variation(fib_seq, threads_count):
    """ Create threads to execute the program with using (only) mutex

    :param fib_seq: array for fibonacci sequence
    :param threads_count: the number of threads

    :rtype: None
    """
    f_i = FibonacciIndex()
    threads = [Thread(compute_fibonacci_without_barrier, f_i, fib_seq, i) for i in range(threads_count)]
    [t.join() for t in threads]


def second_variation(fib_seq, threads_count):
    """ Create threads to execute the program with using turnstile

    :param fib_seq: array for fibonacci sequence
    :param threads_count: the number of threads

    :rtype: None
    """
    barrier1 = TurnstileBarrier(threads_count)
    barrier2 = TurnstileBarrier(threads_count)
    threads = [Thread(compute_fibonacci, barrier1, barrier2, fib_seq, i) for i in range(threads_count)]
    [t.join() for t in threads]


def third_variation(fib_seq, threads_count):
    """ Create threads to execute the program with using event

    :param fib_seq: array for fibonacci sequence
    :param threads_count: the number of threads

    :rtype: None
    """
    barrier1 = EventBarrier(threads_count)
    barrier2 = EventBarrier(threads_count)
    threads = [Thread(compute_fibonacci, barrier1, barrier2, fib_seq, i) for i in range(threads_count)]
    [t.join() for t in threads]


if __name__ == '__main__':
    THREADS = 15
    fib_seq = [0] * (THREADS + 2)
    fib_seq[1] = 1
    first_variation(fib_seq, THREADS)
    second_variation(fib_seq, THREADS)
    third_variation(fib_seq, THREADS)
    print(fib_seq)
