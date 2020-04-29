#!/usr/bin/env python3


import veitch
import read

INPUT_FILE = 'input.txt'


def main():
    for i, inp in enumerate(read.read_inputs(INPUT_FILE)):
        print(f'{i + 1}. {veitch.Diagram(inp).terms}')


if __name__ == "__main__":
    main()
