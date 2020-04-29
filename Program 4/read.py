#!/usr/bin/env python3


def read_inputs(file):
    with open(file) as f:
        for line in f.read().splitlines():
            inp = line.split()
            opponent_markers = inp[:3]
            player_markers = inp[3:6]
            _ = inp[6]  # number of rolls
            rolls = inp[7:]
            yield opponent_markers, player_markers, rolls
