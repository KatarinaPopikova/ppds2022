from fei.ppds import Semaphore, Mutex


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


if __name__ == '__main__':
    thread_count = 5
    sb = SimpleBarrier(thread_count)
