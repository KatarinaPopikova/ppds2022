import matplotlib.pyplot as plt
from collections import Counter
from fei.ppds import Thread, Mutex


class Shared:
    """Shared array for threads"""

    def __init__(self, size):
        """Create shared zero array with the size for increasing.
        Initialize counter to 0. This counter will point to index of array.

        :param size: size of shared array
        """
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared, mutex):
    """ Function for increasing the values of array.

    :param shared: instance of Shared class
    :param mutex: synchronization tool to make the critical area atomically executed
    """
    while True:
        mutex.lock()
        if shared.counter < shared.end:
            shared.elms[shared.counter] += 1
            shared.counter += 1
            mutex.unlock()
        else:
            mutex.unlock()
            break


size = 1_000_000_000
shared = Shared(size)
mutex = Mutex()

t1 = Thread(do_count, shared, mutex)
t2 = Thread(do_count, shared, mutex)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())

plt.hist(shared.elms, bins=len(counter), align='mid')
plt.xticks(range(len(counter)))
plt.show()
