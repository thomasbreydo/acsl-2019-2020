#!/usr/bin/env python3

import adf
import read

# Path to input file (relative to current working directory)
INPUT_PATH = 'input'


def main():
    a, b = read.read_input(INPUT_PATH)
    print(adf.adf(a, b))


if __name__ == "__main__":
    main()
