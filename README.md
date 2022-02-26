# ppds2022

Full subject name:  
**Slovak:** Paralelné programovanie a distribuované systémy  
**English:** Parallel programming and distributed systems

----

Links for [lecture](https://www.youtube.com/watch?v=sR5RWW1uj5g)
, [exercise](https://www.youtube.com/watch?v=vIiHVcb3HqU) on YouTube
and [exercises](https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F) in text form for these
programs.
---

Exercise 2
-----------
*******
**Assignment 1**  
Implement ADT SimpleBarrier according to specifications from the lecture. First try to use ADT Semaphore for
synchronization as it was explained in the lecture. After successful implementation in this way, try to use event
signaling to implement the turnstile.  
Program creates 5 threads that execute the function. This function prints sentences (using function 'print' from
module 'ppds') with meaning "Before barrier" and "After barrier" between implemented barrier.

**Solution**:
Five threads print sentence before barrier with theirs id. They wait for all threads to complete this part of the code
thanks to the implemented barrier. When each thread come to the barrier, barrier releases all of them and threads print
sentence after barrier with theirs id. This functionality is implemented in the function `use_barrier`.

- body of `use_barrier`  
  ![use_barrier body](images/img.png)
- output  
  ![program output](images/img_1.png)

For expected output there will be used two different barriers. The first uses a turnstile, the second event.

*Variation_1*:
Declare a `TurnstileSimpleBarrier` class with thread count, counter, mutex, and turnstile. Turnstile is instance of
Semaphore. If `0` will be sent to Semaphore as a parameter, no thread will pass through the `wait()` method of turnstile
until the `signal()` method is called. Its parameter determines how many threads can pass through the turnstile `wait()`
method. Barrier synchronization is implemented in the `wait()` method of the `TurnstileSimpleBarrier` class. In the
method, it is necessary to counts how many threads evoked this method. We know from the first exercise that the counter
needs to be synchronized. There is a mutex for synchronization. During implementation is necessary to think, how to use
synchronization tools to avoid deadlock. The condition is also checked under lock if the counter has detected all the
threads. If not, the thread releases mutex lock and the turnstile blocks thread to wait for all the threads. However, if
the counter has detected all the threads, the turnstile invokes a `signal()` which also defines how many threads the
barrier will release - whereas all, so the number of created threads.

- turnstile barrier implementation
  ![barrier implementation](images/img_2.png)

*Variation_2*:
The implementation using an instance of the `Event()` class is not very different in the implementation from
Variation_1. Event method `wait()` still blocks threads. The difference is that the event `signal()` method does not
define how many threads the `wait()` method can release, but `wait()` will no longer block threads until the `clear()`
method is called. It is enough to use the barrier once to implement assignment 1, therefore the `clear()` method was not
used.

- event barrier implementation  
  ![barrier implementation](images/img_3.png)
