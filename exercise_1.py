from fei.ppds import Thread, Semaphore, Mutex, print


class SimpleBarrier:
    def __init__(self, thread_count):
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.turnstile = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.turnstile.signal(self.all_thread_count)
        self.mutex.unlock()
        self.turnstile.wait()


def use_barrier(barrier, thread_id):
    print("Thread %d before barrier" % thread_id)
    barrier.wait()
    print("Thread %d after barrier" % thread_id)


if __name__ == '__main__':
    thread_count = 5
    sb = SimpleBarrier(thread_count)
    threads = [Thread(use_barrier, sb, i) for i in range(thread_count)]
    [t.join() for t in threads]
