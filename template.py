#!/usr/bin/env python3
from helpers import (
    read_url as read_url,
    timethis as timethis,
)

URL = "https://adventofcode.com/2023/day/n/input"
TEST = """"""


def parse_thing(input: str) -> str:
    result = ""
    for line in input.strip().split("\n"):
        if line == "^$":
            continue
        result = line
    return result


def solve_thing(input: str) -> None:
    print(input)


if __name__ == "__main__":

    def stage1_test():
        thing = parse_thing(TEST)
        solve_thing(thing)
        pass

    def stage1():
        pass

    def stage2_test():
        pass

    @timethis
    def stage2():
        pass

    stage1_test()
    stage1()
    stage2_test()
    stage2()
