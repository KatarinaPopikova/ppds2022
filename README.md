# ppds2022

Full subject name:  
**Slovak:** Paralelné programovanie a distribuované systémy  
**English:** Parallel programming and distributed systems

***
Links for [lecture](https://www.youtube.com/watch?v=vFLQgRXrA0Q)
and [exercise](https://www.youtube.com/watch?v=kAcKWM4qR6o)  on YouTube
and [exercises](https://uim.fei.stuba.sk/i-ppds/7-cvicenie/) in text form for these programs.
***

Exercise 7
-----------
*******
**Assignment**  
Write an application that will use N (N> 2) coprograms (using advanced generators) and use own scheduler to switch them.

*Solution*:
Program reads a file and find all numbers in this file. Calculates two sums. One for even numbers and the other for odd
numbers. Let this program be implemented using coprograms of advanced generators. We divided the solution as follows:

1. Load a row
2. Create an array of numbers located in the line
3. Divide by number evenness
4. Create a sum 4a. even numbers 4b. odd numbers

The `cat` function accepts the file and coprogram `split_numbers` at the input. Initializes it by calling the `next ()`
function. It reads the rows one by one and sends the coprogram to process. After reading the file The generator's
`close ()` method throws a GeneratorExit exception.

The `split_numbers` coprogram will accepts the `evenness` coprogram at the input and initialize it wilt next() function.
Coprogram `split_numbers` is waiting for the input line of text from the file. When coprogram gets a line, it sends an
array of numbers in that line to next coprogram `evenness`. After receiving the GeneratorExit exception, it forwards
this exception coprogram, which continues to work with found numbers.

The `evenness` coprogram will accepts the two coprograms: `even` and `odd` at the input. At the beginning this two
coprograms are initialized. When coprogram `evenness` gets an array, it goes through the array and sends an even number
to the `even` coprogram and odd to `odd`. After receiving the GeneratorExit exception, it forwards this exception both
coprograms, which continue work with numbers.

Last coprograms `even` and `odd` are waiting for the input number. When some coprogram gets a number, it sums to the
overall even or odd result. After receiving the GeneratorExit exception, the coprogram activity ends by displaying the
result on the screen.