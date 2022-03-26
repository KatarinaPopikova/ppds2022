from fei.ppds import Thread


class Shared:
    def __init__(self):
        pass


def customer():
    pass


def barber():
    pass


if __name__ == '__main__':
    shared = Shared()
    barbers = [Thread(barber, shared) for _ in range(3)]
    customers = [Thread(customer, shared) for _ in range(3)]

    [thread.join() for thread in barbers + customers]
