from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, Event


class FibonacciIndex:
    def __init__(self):
        self.index = 0

    def get_index(self):
        return self.index

    def set_index(self):
        self.index += 1


class TurnstileBarrier:

    def __init__(self, thread_count):
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.count += 1
        self.check_signal()
        self.mutex.unlock()
        self.turnstile.wait()

    def get_all_thread_count(self):
        return self.all_thread_count

    def set_all_thread_count(self):
        self.all_thread_count -= 1
        self.check_signal()

    def check_signal(self):
        if self.count == self.all_thread_count:
            self.count = 0
            self.turnstile.signal(self.all_thread_count)


class EventBarrier:
    def __init__(self, thread_count):
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        if self.count == 0:
            self.event.clear()
        self.count += 1
        self.check_signal()
        self.mutex.unlock()
        self.event.wait()

    def get_all_thread_count(self):
        return self.all_thread_count

    def set_all_thread_count(self):
        self.all_thread_count -= 1
        self.check_signal()

    def check_signal(self):
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()


def compute_fibonacci(barrier1, barrier2, fib_seq, i):
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
    f_i = FibonacciIndex()
    threads = [Thread(compute_fibonacci_without_barrier, f_i, fib_seq, i) for i in range(threads_count)]
    [t.join() for t in threads]


def second_variation(fib_seq, threads_count):
    barrier1 = TurnstileBarrier(threads_count)
    barrier2 = TurnstileBarrier(threads_count)
    threads = [Thread(compute_fibonacci, barrier1, barrier2, fib_seq, i) for i in range(threads_count)]
    [t.join() for t in threads]


def third_variation(fib_seq, threads_count):
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
