#!/usr/bin/env python3


class SubString:
    def __init__(self, master, start, length):
        self.master = master
        self.start = start
        self.length = length
        self.value = master[start: start + length]

    def __lt__(self, other):
        assert self.master == other.master
        return (self.value, self.start) < (other.value, other.start)

    def __str__(self):
        return self.value

    def __repr__(self):
        return f"SubString('{self.master}', {self.start}, {self.length})"

    def isempty(self):
        return self.length < 1

    def find_in(self, master):
        start = master.index(self.value)
        return SubString(master, start, self.length)

    def after_split(self):
        return self.master[:self.start], self.master[self.start + self.length:]


def longest_common_substr(a, b):
    '''Return common substrings as tuple of 2 SubString() objects'''
    len_a = len(a)
    len_b = len(b)

    b_is_longer = len_b > len_a

    longest_substr_a = None
    longest_substr_b = None

    if b_is_longer:
        substr_len = len_a

        while not longest_substr_a:
            for start_i in range(len_a - substr_len + 1):
                match_a = SubString(a, start_i, substr_len)
                try:
                    match_b = match_a.find_in(b)  # error if not found
                except:
                    continue
                else:
                    try:
                        longest_substr_a = min(longest_substr_a, match_a)
                    except:  # longest_substr_a is still None
                        longest_substr_a = match_a
                    try:
                        longest_substr_b = min(longest_substr_b, match_b)
                    except:  # longest_substr_a is still None
                        longest_substr_b = match_b
                        # while loop will finish after all other substrings of
                        # current length are searched
            substr_len -= 1

    else:  # b is not longer
        substr_len = len_b

        while not longest_substr_b:
            for start_i in range(len_b - substr_len + 1):
                match_b = SubString(b, start_i, substr_len)
                try:
                    match_a = match_b.find_in(a)  # error if not found
                except:
                    continue
                else:
                    try:
                        longest_substr_a = min(longest_substr_a, match_a)
                    except:  # longest_substr_a is still None
                        longest_substr_a = match_a
                    try:
                        longest_substr_b = min(longest_substr_b, match_b)
                    except:  # longest_substr_a is still None
                        longest_substr_b = match_b
                        # while loop will finish after all other substrings of
                        # current length are searched
            substr_len -= 1

    return longest_substr_a, longest_substr_b
