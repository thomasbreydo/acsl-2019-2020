import math
import functools

INPUT_FILE = 'input.txt'


def input_gen(filepath):
    with open(filepath) as f:
        for line in f.readlines():
            yield line.split()  # tuple n, p


@functools.lru_cache(maxsize=None)  # memoize
def isprime(x):
    if x <= 1:
        return False
    if x == 2:
        return True
    for i in range(2, math.ceil(math.sqrt(x)) + 1):
        if isprime(i) and x % i == 0:
            return False
    return True


@functools.lru_cache(maxsize=None)
def n_prime_factors(n):
    total = 0
    i = 2
    while not isprime(n) and i <= math.sqrt(n):
        if isprime(i) and n % i == 0:  # IF i IS FACTOR
            while n % i == 0:  # reduce
                n //= i
            total += 1
        i += 1
    if isprime(n):
        total += 1
    return total


def transform(n, p):
    '''``str:num``, ``int:position`` between 1 and # of digits of ``num``.'''
    transformed = ''
    inverse_p = len(n) - p  # p is given from right to left
    pth = int(n[inverse_p])

    past_p = False

    for i, digit in enumerate(n):
        if not past_p:
            if i < inverse_p:  # before p
                transformed += str(int(digit) + pth)
            else:  # at p
                transformed += str(n_prime_factors(int(n)))
                past_p = True
        else:  # past p
            transformed += str(abs(int(digit) - pth))
        i -= 1

    return transformed


def main():
    for n, p in input_gen(INPUT_FILE):
        print(transform(n, int(p)))  # n string by default


if __name__ == "__main__":
    main()
