""""Author: Katarína Stasová
    License: MIT
    Use of multiple synchronization objects in the program. The sensors update the data and the monitors display them
    updated in the power plant."""

from fei.ppds import Thread


class Shared():
    def __init__(self):
        pass


def monitor(thread_name):
    print("%s" % thread_name)


def sensor(thread_name):
    print("%s" % thread_name)


if __name__ == '__main__':
    threads = list()
    for i in {'P', 'T', 'H'}:
        t = Thread(sensor, '%s' % i)
        threads.append(t)

    for i in range(8):
        t = Thread(monitor, '%d' % i)
        threads.append(t)

    for t in threads:
        t.join()
