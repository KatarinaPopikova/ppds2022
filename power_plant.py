""""Author: Katarína Stasová
    License: MIT
    Use of multiple synchronization tools in the program (also use mutual exclusion). The sensors update the data and
    the monitors display them updated in the power plant to the operators."""

from random import randint
from time import sleep

from fei.ppds import Thread, Semaphore, Mutex, print, Event


class Lightswitch:
    """ Provides access to only one category. """

    def __init__(self):
        """Lightswitch initialization.
        mutex - synchronization tool to make the critical area atomically executed
        counter - number of threads from a category in the area """
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        """ Count threads from a category in the area.
            If the area is occupied by another category, the first thread it finds is waiting for a semaphore and
            holding a mutex.

        :param sem: Semaphore
        :return: the number of threads from a category in the area
        """
        self.mutex.lock()
        counter = self.counter
        if self.counter == 0:
            sem.wait()
        self.counter += 1
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        """ Subtract threads from a category in the area.
            If the last thread leaves the area (from threads that entered), it releases the occupation with a semaphore.

        :param sem: Semaphore
        :return: the number of threads from a category in the area
        """
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


class EventBarrier:
    """"A reusable barrier for waiting for all sensors to complete the part of code. It uses event. """
    def __init__(self, thread_count):
        """Event barrier initialization:
         all_thread_count - the number of sensors
         count - the number of waiting threads in event
         mutex - synchronization tool to make the critical area atomically executed
         event - synchronization tool to management threads

        :param thread_count: the number of sensors
        """
        self.all_thread_count = thread_count
        self.count = 0
        self.mutex = Mutex()
        self.event = Event()

    def wait(self):
        """Waiting until all sensors have completed part of the code.
        Between locked mutex is code automatically executed.
        The event method wait() blocks all threads, which invoke it, until method signal() happened.
        The event method clear() activates wait(), when each thread is released from the barrier.
        """
        self.mutex.lock()
        self.count += 1
        if self.count == self.all_thread_count:
            self.count = 0
            self.event.signal()
            self.event.clear()
        last = self.count
        self.mutex.unlock()

        if last:
            self.event.wait()


class Shared:
    """" Shared class for sensors and monitors (all threads)."""
    def __init__(self, sensor_count):
        """ valid_data- causes the monitors to start displaying data only when each sensor updates it for the first time
            turnstile- helps to change the category
            ls_monitor- occupies the monitor area
            ls_sensor- occupies the sensor area
            access_data- informs whether the category can occupy an area or is already occupied and must waits
            event- wait for all sensors

            :param sensor_count: the number of sensors

        """
        self.valid_data = Semaphore(0)
        self.turnstile = Semaphore(1)
        self.ls_monitor = Lightswitch()
        self.ls_sensor = Lightswitch()
        self.access_data = Semaphore(1)
        self.barrier = EventBarrier(sensor_count)


def monitor(shared, thread_name):
    """ Simulation, that monitors reading the data and displays to operators. They read data between 40 to 50ms.
    Data reading does not start until each sensor updates the data for the first time.
    Monitors can read when no sensors updating.


    :param shared: shared class for all threads
    :param thread_name: the monitor id
    """
    shared.valid_data.wait()
    while True:
        shared.turnstile.wait()
        shared.turnstile.signal()
        count = shared.ls_monitor.lock(shared.access_data)
        time = randint(4, 5) / 100
        # simulation of reading data
        sleep(time)
        print('monit "%s": number_of_reading_monitors = %2d,reading_duration = %0.3f' % (thread_name, count, time))
        shared.ls_monitor.unlock(shared.access_data)


def sensor(shared, thread_name, monitor_count):
    """ Simulation, that sensors wait 50-60ms between updating data.
        Sensor with name H updating 20-25ms and P, T updating 10-20ms. After the update they are waiting for each other
        and let know that monitors can start reading.
        Sensors can update when no monitors reading.

    :param shared: shared class for all threads
    :param thread_name: the sensor name
    :param monitor_count: the number of monitors
    """
    while True:
        sleep(randint(5, 6) / 100)
        shared.turnstile.wait()
        count = shared.ls_sensor.lock(shared.access_data)
        shared.turnstile.signal()

        if thread_name == 'H':
            time = randint(20, 25) / 1000
        else:
            time = randint(1, 2) / 100
        print('sensor "%s": number_of_writing_sensors = %2d, writing_duration = %0.3f' % (thread_name, count, time))
        # simulation of writing data
        sleep(time)
        shared.ls_sensor.unlock(shared.access_data)
        shared.barrier.wait()
        shared.valid_data.signal(monitor_count)


if __name__ == '__main__':
    """Create threads as:
     -monitors,
     -sensors.
     The sensors are used to simulate updating the measured values. 
     The monitors are used to display data to the operator.
     """
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
