# ppds2022

Full subject name:  
**Slovak:** Paralelné programovanie a distribuované systémy  
**English:** Parallel programming and distributed systems

***
Links for [lecture](https://www.youtube.com/watch?v=Vvzh2N31EyQ)
, [exercise](https://www.youtube.com/watch?v=iotYZJzxKf4) on YouTube
and [exercises](https://uim.fei.stuba.sk/i-ppds/5-cvicenie-problem-fajciarov-problem-divochov-%f0%9f%9a%ac/) in text
form for these programs.
***

Exercise 3
-----------
*******
**Assignment 2- Savages problem**

The savages eat serving from the pot. When the savage find out that all the servings are over, he wakes up the chefs and
the savages wait to the full pot. The chefs help each other with cooking. They fill the pot and when is full, the
savages can continue in eating. Only one chef signals to savage, that the pot is full.

*Solution*:
This is a modified version of the synchronization task: producers-consumers. The two categories are mutually exclusive
in a certain run. When the savages eat, the chefs wait. And when the chefs cook, the savages wait.

The savages take a portion gradually and can eat in parallel / competitively. Whereas it is necessary to count the
removed portions to we know when the pot is empty, the removal of the portion is protected by a mutex. If the savage
finds that the pot is empty, he wakes up all the chefs and waits for the semaphore until the pot is full. At the same
time, he holds a mutex and the other savages have to wait until the savage waiting at the semaphore releases the mutex.
The savage who finds that the pot is empty allows as many chefs to go through the another semaphore as there are. They
cook together and when they finish their work, they wait on the (reusable) barrier (we use implementation according
to ** Tomáš Popík ** from the [lecture]
(https://www.youtube.com/watch?v=WcaVHQM8zVo&t=901shttps://www.youtube.com/watch?v=WcaVHQM8zVo&t=901s)). The last who
enters to the barrier fills the pot and unlocks the semaphore for the savage. The savages can continue to eat while the
chefs wait for the semaphore until a savage informs them again about the empty pot. This happens in a cycle. 


**Pseudocode**  

```
Initialize savage_count to 10
Initialize servings_count to 3
Initialize chefs_count to 5

CLASS Shared
    servings = count of servings
    mutex = Mutex
    empty_pot = Semaphore to 0
    full_pot = Semaphore to 0
    barrier = EventBarrier to chefs_count
END CLASS

FUNCTION savage:
INPUT: savage_id, shared, chefs_count
    WHILE true:
        lock area
        IF servings are 0:
            signal empty_pot to chefs_count
            wait for full_pot
        END IF
        decrease servings 
        unlock area
        eat
    END WHILE
END FUNCTION

FUNCTION chef:
INPUT: Shared, thread_name, monitor_count
    wait for each thread to write data and valid_data invokes a signal
    WHILE true:
        wait for empty_pot
        cooking
        wait for all chefs
    END WHILE
END FUNCTION

```