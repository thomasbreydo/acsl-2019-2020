#!/usr/bin/env python3

import re
NONALPHA = re.compile('[^a-zA-Z]')


def _clean(string):
    return NONALPHA.sub('', string).upper()


def read_input(file):
    with open(file) as f:
        return [_clean(line) for line in f.read().splitlines()]
