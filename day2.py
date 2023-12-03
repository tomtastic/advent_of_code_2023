#!/usr/bin/env python3
import requests

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
URL = "https://adventofcode.com/2023/day/2/input"
MAXIMUMS = {"red": 12, "green": 13, "blue": 14}
TEST = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""


def read_cookie(file: str) -> str:
    """Get the AdventOfCode session cookie we saved earlier"""
    with open(file, mode="r") as f:
        return f.read().strip()


def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""
    session_cookie = {"session": read_cookie(COOKIEFILE)}
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text


def is_cube_set_possible(cubes: dict) -> bool:
    """Return true if all cube values are less than maximums"""
    if (
        cubes.get("red", 0) > MAXIMUMS["red"]
        or cubes.get("blue", 0) > MAXIMUMS["blue"]
        or cubes.get("green", 0) > MAXIMUMS["green"]
    ):
        return False
    return True


def are_gamesets_possible(game_sets: str) -> bool:
    """Takes a semi-colon separated list of games"""
    """Generate a list of game set possibilities"""
    game_set_possibilities = list()
    for cube_set in game_sets.split(";"):
        cubes = dict(
            (v, int(n)) for n, v in (a.strip().split(" ") for a in cube_set.split(","))
        )
        game_set_possibilities.append(is_cube_set_possible(cubes))
    if all(game_set_possibilities):
        return True
    else:
        return False


def min_powers(game_sets: str) -> int:
    """Takes a semi-colon separated list of games"""
    """Generate sum of min cubes required for all games"""
    min_set = {"red": 0, "green": 0, "blue": 0}
    for cube_set in game_sets.split(";"):
        cubes = dict(
            (v, int(n)) for n, v in (a.strip().split(" ") for a in cube_set.split(","))
        )
        for key in cubes.keys():
            if cubes[key] > min_set[key]:
                min_set[key] = cubes[key]
    power = 1
    for v in min_set.values():
        power = power * v
    return power


def solve(input: str) -> dict:
    """Return both;
    - the sum of game IDs where all game sets are true
    - the sum of min powers
    """
    sum_possible = 0
    sum_powers = 0
    for line in input.split("\n"):
        if ":" not in line:
            continue
        game_num, game_sets = line.split(":", 2)
        game_num = int(game_num.split()[1])
        # Part 1
        if are_gamesets_possible(game_sets):
            sum_possible += game_num
        # Part 2
        sum_powers += min_powers(game_sets)
    return {"possible": sum_possible, "powers": sum_powers}


if __name__ == "__main__":
    puzzle_input = read_url(URL)

    print(f"Sum of game IDs for TEST input: {solve(TEST)['possible']}")
    print(f"Sum of min powers for TEST input: {solve(TEST)['powers']}")
    print()
    print(f"Sum of game IDs for puzzle input: {solve(puzzle_input)['possible']}")
    print(f"Sum of min powers for puzzle input: {solve(puzzle_input)['powers']}")
