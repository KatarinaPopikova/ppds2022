
import re


def cat(f, next_fnc):
    next(next_fnc)
    for line in f:
        next_fnc.send(line)
    next_fnc.close()


def split_numbers(next_fnc):
    next(next_fnc)
    try:
        while True:
            line = (yield)
            next_fnc.send(re.findall('[0-9]+', line))
    except GeneratorExit:
        next_fnc.close()


def evenness(next_fnc1, next_fnc2):
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
    even_sum = 0
    try:
        while True:
            even_sum += (yield)
    except GeneratorExit:
        print("Sum of even numbers: %d" % even_sum)


def odd():
    odd_sum = 0
    try:
        while True:
            odd_sum += (yield)
    except GeneratorExit:
        print("Sum of odd numbers: %d" % odd_sum)


def main():
    f = open('resource/barber.txt')

    e = even()
    o = odd()
    e_ness = evenness(e, o)
    no = split_numbers(e_ness)

    cat(f, no)


if __name__ == '__main__':
    main()
