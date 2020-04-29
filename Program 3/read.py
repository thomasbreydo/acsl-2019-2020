#!/usr/bin/env python3


def read_inputs(file):
    with open(file) as f:
        for line in f.read().splitlines():
            yield int(line, 16)
