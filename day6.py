#!/usr/bin/env python3
from helpers import timethis as timethis, read_url as read_url
import math

# Session cookie is valid for 10 years!
URL = "https://adventofcode.com/2023/day/6/input"
TEST = """Time:      7  15   30
Distance:  9  40  200"""


def get_races(input: str) -> list:
    time = list()
    distance = list()
    for line in input.strip().split("\n"):
        fields = line.split()
        if "Time" in fields[0]:
            time = fields[1:]
        if "Distance" in fields[0]:
            distance = fields[1:]
    races = list(zip(time, distance))
    return races


def get_races_stage2(input: str) -> list:
    time = ""
    distance = ""
    for line in input.strip().split("\n"):
        fields = line.split()
        if "Time" in fields[0]:
            time = "".join(fields[1:])
        if "Distance" in fields[0]:
            distance = "".join(fields[1:])
    races = [time, distance]
    return races


def results(race: list) -> list:
    time = int(race[0])
    results = list()
    if time % 2 == 0:
        # Calc the full list
        for held in range(0, time):
            left = time - held
            if held == 0:
                went = 0
            else:
                went = left * held
            results.append(went)
    else:
        # We can optimise by only doing the first half
        halfway = int(time / 2) + 1
        for held in range(0, halfway):
            left = time - held
            if held == 0:
                went = 0
            else:
                went = left * held
            results.append(went)
        results.extend(reversed(results))
    return results


def strategies(results: list, record: int):
    ways = 0
    for i in results:
        if int(i) > record:
            ways += 1
    return ways


if __name__ == "__main__":

    def stage1_test():
        races = get_races(TEST)
        print(f"Stage1 (example) : {races}")
        ways_to_beat = [strategies(results(x), int(x[1])) for x in races]
        print(math.prod(ways_to_beat))

    def stage1():
        races = get_races(read_url(URL))
        print(f"Stage1           : {races}")
        ways_to_beat = [strategies(results(x), int(x[1])) for x in races]
        print(math.prod(ways_to_beat))

    def stage2_test():
        races = get_races_stage2(TEST)
        print(f"Stage2 (example) : {races}")
        print(strategies(results(races), int(races[1])))

    def stage2():
        races = get_races_stage2(read_url(URL))
        print(f"Stage2           : {races}")
        print(strategies(results(races), int(races[1])))

    stage1_test()
    stage1()
    stage2_test()
    stage2()
