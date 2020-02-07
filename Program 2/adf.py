#!/usr/bin/env python3


from substring import longest_common_substr


def adf(str1, str2):
    total = 0
    substr1, substr2 = longest_common_substr(str1, str2)

    if substr1.isempty():
        return 0

    one, two = substr1.after_split()
    three, four = substr2.after_split()

    if one and three:
        total += adf(one, three)

    if two and four:
        total += adf(two, four)

    return total + substr1.length
