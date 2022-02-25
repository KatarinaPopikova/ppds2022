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

Exercise 1
-----------
*******
**Assignment 1**  
Implement ADT SimpleBarrier according to specifications from the lecture. First try to use ADT Semaphore for
synchronization as it was explained in the lecture. After successful implementation in this way, try to use event
signaling to implement the turnstile.  
Program creates 5 threads that execute the function. This function prints sentences (using function 'print' from
module 'ppds') with meaning "Before barrier" and "After barrier" between implemented barrier.
