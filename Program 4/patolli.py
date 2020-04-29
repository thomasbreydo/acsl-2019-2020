#!/usr/bin/env python3


import primes


class Marker:
    def __init__(self, index, player):
        self.index = index
        self.player = player


class Location:
    def __init__(self, label, occupied=False):
        self.label = label
        self.occupied = occupied


class Game:
    def __init__(self, markers, locations):
        assert isinstance(markers, dict)
        self.markers = markers
        self.locations = locations

    def roll(self, n, player):
        try:
            lowest_marker = min(
                self.markers[player], key=lambda mkr: mkr.index)
        except ValueError:  # player out of markers
            print('ERROR CAUGHT')
            return
        new_location = self.locations[lowest_marker.index + n]
        if new_location.label == 52:  # keep in roll() to use player
            self.markers[player].remove(lowest_marker)
            return
        self.try_move(lowest_marker, new_location)

    def try_move(self, marker, location):
        # full or past 52
        if (location.occupied or location.label > self.locations[-1].label):
            return
        if primes.isprime(location.label):
            # move up to 6 spaces ahead
            for i in range(1, 6):
                if self.locations[marker.index + i].occupied:
                    marker.index += i - 1  # space before this occupied one

                    return

    def force_move(self, marker, new_location):
        self.locations[marker.index].occupied = False
        marker.index = new_location.label - 1
        self.locations[marker.index].occupied = True


if
