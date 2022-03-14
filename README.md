# ppds2022

Full subject name:  
**Slovak:** Paralelné programovanie a distribuované systémy  
**English:** Parallel programming and distributed systems

***
Links for [lecture](https://www.youtube.com/watch?v=8CF098hseDw&t=457s)
, [exercise](https://www.youtube.com/watch?v=DgI8E_bVfBA) on YouTube
and [exercises](https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/)
in text form for these programs.
***

Exercise 4
-----------
*******
**Assignment**

The nuclear power plant has 3 sensors:

one primary circuit coolant flow sensor (sensor P)
one primary circuit coolant temperature sensor (T sensor)
one control rod insertion depth sensor (sensor H)

These sensors are constantly trying to update the measured values. They save the data in a common data repository. Each
sensor has its own dedicated space in the storage, where it saves data (consider in synchronizing).

The sensors update every 50-60 ms. The data update takes 10-20 ms for sensor P and T, but it takes 20-25 ms for sensor
H.

In addition to the sensors, there are eight operators in that power plant, who are constantly looking at own monitor to
see where the measured values of the sensors are displayed. The monitor sends a data update request continuously and
continuously in a cycle. One update takes 40-50 ms.

Monitors can start working if all sensors have already updated valid data.

1. Analyze what types of synchronization tools (or their modifications or combinations) are involved in this assignment.
2. Exactly map the synchronization tools of your choice to the individual parts of the assignment.
3. Write the pseudocode of the problem solution.
4. Write a program that will suitably model this synchronization task.
5. Add listings:
    - before simulating a data update: 'sensor "% 02d": number_of_writing_sensors =%02d, writing_duration =% 03d \ n'
    - when reading data: 'monit "% 02d": number_of_reading_monitors =% 02d, reading_duration =% 03d \ n'

**1. Analyze the synchronization tools**  
*Lightswitch* - This tool is useful if you want to exclude categories from each other in a certain part of the code. In
our case, we want to exclude that if the sensors update the data, the monitors cannot update it. Also, if the monitors
are reading data, the sensors cannot update them. Sensors can work at the same time, monitors can work at the same time,
but not with sensors.

Sensors have own lightswitch and monitors own. But both categories use one common semaphore.

The `lock ()` method cares that a category occupies an area when it can work, and the second category must wait for that
area at that moment. Therefore, when the first thread from one category enters this method, it uses a mutex (make the
critical area atomically executed) and finds out from the semaphore with the `wait ()` method whether the area is
occupied or can occupy it for itself. If it is occupied, the thread (monitor) waits on the semaphore and holds the
mutex, so other threads in this category cannot follow this thread. If the semaphore allows continuing, it means that
the area is already free and the other threads will no longer stop at the semaphore. The counter is in charge of this
activity. The counter is responsible that other threads in this category do not stop at the semaphore until the room is
empty.

The `unlock()` method call threads, when they leave the area. Because they reduce the number of fibers in the region,
the counter is protected by a mutex. If the last thread leaves the area, it will let the semaphore know that it can
allow the nearest category let into the area.

*Semaphore* - the semaphore releases threads through the `wait()` method if its value is positive. It releases them as
long as its value is positive. This method will then reduce its value. However, if the semaphore value is not positive,
the threads wait on the `wait()` method. The next `signal()` method increases the semaphore value.

*Turnstile* - This synchronization tool management threads. It releases the threads one by one. In order not to starve
one category, the turnstile will help to change the categories.

*Reusable barrier* - This tool waits and blocks threads, until a certain number of threads complete the part of code. We
use implementation according to **Tomáš Popík**  from
the [lecture](https://www.youtube.com/watch?v=WcaVHQM8zVo&t=901shttps://www.youtube.com/watch?v=WcaVHQM8zVo&t=901s). In
method `wait()` is counting the number of threads. Counter is under mutex. When counter reaches the certain number of
threads, last threads invoke Event `signal()` method, and release threads, which where blocked on `wait()` method of
Event. Also invoke Event method `clear()` to activates blocking.

**2. Map the synchronization tools**  
At the beginning, the monitors wait on the semaphore until each sensor updates the data.  
Sensors in the loop wait 50-60ms, gradually pass through the turnstile. In the turnstile, they either occupy or reserve
the area using a lightswitch. However, the monitors have not yet started, they will lock the area. After writing the
data, they gradually unlock the lightswitch and everyone waits on the barrier. The last sensor releases the area, the
barrier releases the threads, and a signal is sent to the monitor that they can read the data. The barrier will ensure
that the sensors do not write data 50-60ms, when they together wait since the last sensor writes. This is repeated in
the `sensor()` method, but from now the sensors must fight for the area to write data again.  
The monitors gradually pass through the turnstile, and after it try to occupy the area through the lightswitch. After
reading, the lightswitch will gradually unlock and last monitor will free up the area for other (/same) categories. This
also happens in a cycle in `monitor()` method.

Sensors can wait max 100ms to update. Example: When sensor is trying to update after 60ms, the monitors read 50ms, so
can read 50ms again, the sensors then wait for the monitor to complete reading last 40ms. That's a total of 100ms.


**3. Pseudocode**  

```
CLASS Shared
    valid_data = Semaphore to 0
    turnstile = Semaphore to 1
    ls_monitor = Lightswitch
    ls_sensor = Lightswitch
    access_data = Semaphore to 1
    barrier = EventBarrier to sensor_count
END CLASS

FUNCTION monitor:
INPUT: Shared, thread_name
    wait for each thread to write data and valid_data invokes a signal
    WHILE true:
      enter the turnstile when it is free
      release the turnstile
      try to occupy the area for the category of monitors throught ls_monitor with access_data
      read data 40-50ms
      print monitor id, number of monitors reading, reading length
      free the area throught ls_monitor with access_data
    END WHILE
END FUNCTION

FUNCTION sensor:
INPUT: Shared, thread_name, monitor_count
    wait for each thread to write data and valid_data invokes a signal
    WHILE true:
      wait 50-60ms
      enter the turnstile when it is free
      try to occupy the area for the category of sensors throught ls_sensor with access_data
      release the turnstile
      write data| if H: 20-25ms, if P or T 10-20ms
      print sensor id, number of monitors reading, writing length
      free the area throught ls_sensor with access_data
      wait for all the threads with the barrier
      valid_data invokes the signal and releases waiting monitor threads on valid_data
    END WHILE
END FUNCTION

```

