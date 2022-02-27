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
module 'ppds', which using lock for a comprehensive print) with meaning "Before barrier" and "After barrier" between
implemented barrier.

**Solution**:
Five threads print sentence before barrier with theirs id. They wait for all threads to complete this part of the code
thanks to the implemented barrier. When each thread come to the barrier, barrier releases all of them and threads print
sentence after barrier with theirs id. This functionality is implemented in the function `use_barrier`.

- body of `use_barrier`  
  ![use_barrier body](images/img.png)
- output  
  ![program output](images/img_1.png)

For expected output there will be used two different type of barriers. The first uses a turnstile, the second event.

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

**Assignment 2**
Use the same principle as in assignment 1, but the print is executed in a loop.

**Solution**:
For implementation is needed reusable barrier. Therefore, the barriers from assignment 1 will be reprogrammed. All
threads executing function. Each of thread print the sentence before barrier with id. Barrier waits for all threads.
Each of thread prints the sentence after barrier with id. Barrier again waits for all threads. This is executed in the
cycle.

- body of `use_barrier`  
  ![use_barrier body](images/img_4.png)
- output  
  ![program output](images/img_5.png)

Each of thread has to executed `rendezvous()`, subsequently `ko()` and it is executed in the loop.  
For expected output there are three variations implemented in the file "assignment_2":

- used two instances of the class `TurnstileBarrier`- using turnstile
- used two instances of the class `EventBarrier`- using event
- used only one instance of the class `EventBarrier2`- using event

*Variation_1*:
In the method `first_variation()` are initialized two instances of the class `TurnstileBarrier` and created the value
of `thread_count` (5) threads. Threads call `use_two_barriers`, which differs from `use_barrier`, because in this
variation is needed 2 different barriers (two turnstiles).

- body of `use_two_barrier`  
  ![use_barrier body](images/img_6.png)

The `TurnstileSimpleBarrier` class is reprogrammed to be reusable. So when the last thread calls the `wait()` method
of `TurnstileBarrier` instance and the counter has the same value as is the number of threads, counter is restarted.
Afterwards is invoked the `signal()` method of turnstile. It identifies how many threads can release `wait()` method of
turnstile. If in `use_two_barriers()` was not used second instance, it would not be a correctly implemented parallelism.
For example, if one thread overtakes the thread which triggered the signal (so one thread is possible to execute part of
code twice and other none). If two instances are used, the next barrier does not invoke a signal until the last thread
calls wait on that barrier (and the second counter has the same value as the number of threads).

- turnstile barrier implementation  
  ![barrier implementation](images/img_7.png)

*Variation_2*:
In this variation is also used the `use_two_barriers` method with instances of the `EventBarrier` class. It is for the
same reason as with `TurnstileBarrier`. Difference is in the implementation of the wait method of  `EventBarrier`. The
thread which invokes this method in the serial part (under lock) increases the counter by 1 and if the value of the
counter is not equal to the number of threads, it waits on `wait()` event method. The last threads invokes signal and
the `wait()` method is inactive until `clear()` is invoked.  
To prevent the last thread from being blocked, we create the opposite counter after the `wait()` event method. When the
counter is set to 0, the clear method is called. If we used only one instance of this class, the next time the barrier
was used, the thread that came out of the `wait()` of EventBarrier method and overtook the others would increment the
counter, when `clear()` method is not called, and parallelism would not be maintained. With two barriers, the last
thread will be waited for, so parallelism will be preserved.

- event barrier implementation  
  ![barrier implementation](images/img_8.png)

*Variation_3*:
In this variation is program implemented to use only one instance of the `EventBarrier2` class. Now is
used `use_barrier()` method. So 

- event barrier implementation  
  ![barrier implementation](images/img_9.png)