# ppds2022

Full subject name:  
**Slovak:** Paralelné programovanie a distribuované systémy  
**English:** Parallel programming and distributed systems

***
Links for [lecture](https://www.youtube.com/watch?v=ChtCC15qDgQ)
and [exercise](https://www.youtube.com/watch?v=2o11BPLu9_0&t=322s)  on YouTube
and [exercises](https://uim.fei.stuba.sk/i-ppds/cvicenie-10-cuda-prudy-a-udalosti/) in text form for these programs.
***

Exercise 10
-----------
*******
**Assignment**   
Modify the program from last week:

1) make optimal use of the device and
2) you use streams in the solution.
   Use events to measure time calculations.

*Solution*:
We expanded the previous exercise 9 to find the average of two images but for multiple images. We tried to optimize the
work with the graphics card. Unfortunately, we only used a simulation of the graphics card's behavior, so we can't
take advantage of events or find out the actual optimization by elapsed time.

After loading images into arrays, we create as many CUDA streams as we have arrays, because we want one array to be
processed in one stream on the graphics card.

```python
for _ in range(NUM_ARRAYS):
    streams.append(cuda.stream())
```

Kernels running in different streams can run competitively on the device, so the device should be better used and more
kernels can run at the same time. If we want the data to belong to one stream, we determine which stream the data
belongs to. We also create a memory for the device.

```python
for k in range(NUM_ARRAYS):
    imgs1_output_gpu.append(cuda.to_device(imgs1_output[k], stream=streams[k]))
    img2_gpu.append(cuda.to_device(imgs2[k], stream=streams[k]))
```

Also, if we want to run the kernel, we will say in which stream it is running. So this kernel is called so many times as
many we want averages images.

```python
my_kernel[block_per_grid, thread_per_block, streams[k]](imgs1_output_gpu[k], img2_gpu[k])
```

When we want to get the data back, we catch the data and read which stream it belongs to.

```python
for k in range(NUM_ARRAYS):
    img1_gpu_out.append(imgs1_output_gpu[k].copy_to_host(stream=streams[k]))
```

When we run the program, it elapsed 12,64s. But if we run the same program without using the streams, it elapses 13,66s.
This is also the same duration. If we were to run this program on a real device, we should see acceleration. Because the
kernel is small and does not contain many registers or multiprocessors, all computing elements of the graphics card
should be activated.

The following screen shows the result of the program. The first two are the original images and their average is on the
right.
![Solution](doc/img.png)
