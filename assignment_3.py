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


if __name__ == '__main__':
    THREADS = 5
    fib_seq = [0] * (THREADS + 2)
    fib_seq[1] = 1
    f_i = FibonacciIndex()
    threads = [Thread(compute_fibonacci_without_barrier, f_i, fib_seq, i) for i in range(THREADS)]
    [t.join() for t in threads]
    print(fib_seq)
