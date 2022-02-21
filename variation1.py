import matplotlib.pyplot as plt
from collections import Counter
from fei.ppds import Thread, Mutex


class Shared:
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(shared):
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1


size = 1_000_000
shared = Shared(size)

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())

plt.hist(shared.elms, bins=len(counter), align='mid')
plt.xticks(range(len(counter)))
plt.show()
