from time import sleep
from random import randint
from fei.ppds import Thread, Semaphore, Mutex, Event


def compute_fibonacci(fib_seq, i):
    sleep(randint(1, 10) / 10)
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]


if __name__ == '__main__':
    THREADS = 5
    fib_seq = [0] * (THREADS + 2)
    threads = [Thread(compute_fibonacci, fib_seq, i) for i in range(THREADS)]
    [t.join() for t in threads]
    print(fib_seq)
