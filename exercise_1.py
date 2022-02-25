from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    def __init__(self, thread_count):
        self.N = thread_count
        self.C = 0
        self.M = Mutex()
        self.T = Semaphore(0)

    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal(self.N)
        self.M.unlock()
        self.T.wait()


def use_barrier(barrier, thread_id):
    print("Thread %d before barrier" % thread_id)
    barrier.wait()
    print("Thread %d after barrier" % thread_id)


if __name__ == '__main__':
    thread_count = 5
    sb = SimpleBarrier(thread_count)
    threads = [Thread(use_barrier, sb, i) for i in range(thread_count)]
    [t.join() for t in threads]
