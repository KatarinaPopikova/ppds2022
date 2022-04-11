""""Author: Katarína Stasová
    License: MIT
    Program reads a file and find all numbers in this file. Calculates two sums. One for even numbers and the other for
    odd numbers.

"""
import re


def cat(f, next_fnc):
    """ This is a function that reads the file line by line.
     An "initialization" of coprogram is created by calling the next () function.
     Each line sends the next_fnc () coprogram to process.
     When the input file rows are finished, the generator to which it sends data ends.
     The generator's close () method  throws a GeneratorExit exception.

    :param f: file
    :param next_fnc: this coprogram is sent line by line
    """
    next(next_fnc)
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def split_numbers(next_fnc):
    """ Coprogram, waiting for the input line of text from the file.
        An "initialization" of next coprogram is created by calling the next () function.
        When coprogram gets a line, it sends an array of numbers in that line to next coprogram.
        After receiving the GeneratorExit exception, it forwards this exception
        coprogram, which continues to work with found numbers.

    :param next_fnc: the found numbers are sent as array to this coprogram
    """
    next(next_fnc)
    try:
        while True:
            line = (yield)
            next_fnc.send(re.findall('[0-9]+', line))
    except GeneratorExit:
        next_fnc.close()


def evenness(next_fnc1, next_fnc2):
    """ Coprogram as a planner, waiting for the input array of numbers.
        An "initialization" of next coprograms is created by calling the next () function.
        When coprogram gets an array, it goes through the array and sends an even number to the next_fnc1 coprogram and
        odd to next_fnc2.
        After receiving the GeneratorExit exception, it forwards this exception both
        coprograms, which continue work with numbers.

    :param next_fnc1: the even number is sent to this coprogram next_fnc1
    :param next_fnc2: the odd number is sent to this coprogram next_fnc2
    """
    next(next_fnc1)
    next(next_fnc2)
    try:
        while True:
            numbers = (yield)
            for number in numbers:
                number = int(number)
                if number % 2 == 0:
                    next_fnc1.send(number)
                else:
                    next_fnc2.send(number)

    except GeneratorExit:
        next_fnc1.close()
        next_fnc2.close()


def even():
    """ Coprogram, waiting for the input even number.
        When coprogram gets a number, it sums to the overall even result.
        After receiving the GeneratorExit exception, the coprogram activity ends
        by displaying the result on the screen.
    """
    even_sum = 0
    try:
        while True:
            even_sum += (yield)
    except GeneratorExit:
        print("Sum of even numbers: %d" % even_sum)


def odd():
    """ Coprogram, waiting for the input odd number.
        When coprogram gets a number, it sums to the overall odd result.
        After receiving the GeneratorExit exception, the coprogram activity ends
        by displaying the result on the screen.
    """
    odd_sum = 0
    try:
        while True:
            odd_sum += (yield)
    except GeneratorExit:
        print("Sum of odd numbers: %d" % odd_sum)


def main():
    """ The main function opens the file and initializes the necessary functions."""
    f = open('resource/barber.txt')

    e = even()
    o = odd()
    e_ness = evenness(e, o)
    no = split_numbers(e_ness)

    cat(f, no)


if __name__ == '__main__':
    main()
