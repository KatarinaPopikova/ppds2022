""""Author: Katarína Stasová
    License: MIT
    Use of multiple synchronization objects in the program. The sensors update the data and the monitors display them
    updated in the power plant."""

from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, Mutex, print, Event


class Lightswitch:
    def __init__(self):
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


class EventBarrier:

    def __init__(self, thread_count):
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()
        last = self.count
        self.mutex.unlock()

        if last:
            self.event.wait()


class Shared:
    def __init__(self, sensor_count):
        self.valid_data = Semaphore(0)
        self.turnstile = Semaphore(1)
        self.ls_monitor = Lightswitch()
        self.ls_sensor = Lightswitch()
        self.access_data = Semaphore(1)
        self.event = EventBarrier(sensor_count)


def monitor(shared, thread_name):
    shared.valid_data.wait()
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()
        count = shared.ls_monitor.lock(shared.access_data)
        time = randint(4, 5) / 100
        sleep(time)
        print('monit "%s": number_of_reading_monitors = %2d,reading_duration = %0.3f' % (thread_name, count, time))
        shared.ls_monitor.unlock(shared.access_data)


def sensor(shared, thread_name, monitor_count):
    while True:
        sleep(randint(5, 6) / 100)
        shared.turnstile.wait()
        count = shared.ls_sensor.lock(shared.access_data)
        shared.turnstile.signal()

        if thread_name == 'H':
            time = randint(1, 2) / 100
        else:
            time = randint(20, 25) / 1000
        print('sensor "%s": number_of_writing_sensors = %2d, writing_duration = %0.3f' % (thread_name, count, time))
        sleep(time)
        shared.ls_sensor.unlock(shared.access_data)
        shared.event.wait()
        shared.valid_data.signal(monitor_count)


if __name__ == '__main__':
    MONITOR_COUNT = 8
    SENSOR_NAMES = {'P', 'T', 'H'}
    shared = Shared(3)
    threads = list()

    for i in range(MONITOR_COUNT):
        t = Thread(monitor, shared, '%d' % i)
        threads.append(t)

    for i in SENSOR_NAMES:
        t = Thread(sensor, shared, '%s' % i, MONITOR_COUNT)
        threads.append(t)

    for t in threads:
        t.join()
