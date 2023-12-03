#!/usr/bin/env python3
import requests
from re import finditer

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
URL = "https://adventofcode.com/2023/day/3/input"
TEST = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""


def read_cookie(file: str) -> str:
    """Get the AdventOfCode session cookie we saved earlier"""
    with open(file, mode="r") as f:
        return f.read().strip()


def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""
    session_cookie = {"session": read_cookie(COOKIEFILE)}
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text


def create_map(schematic: str) -> tuple:
    """Parse the schematic and return a tuple of :
    - parts locations
    - symbol locations
    """
    engine_parts_map = list()
    engine_symbols_map = list()
    for line in schematic.split("\n"):
        # Each line in the schematic is 140 chars
        LENGTH = len(line) - 1
        # Dont do regex.findall() here, we get the locations of all matches
        # with finditer(). eg.
        # parts.span() = (index, index+len+1)
        # parts.group() = matched string
        parts_iterable = finditer("[0-9]+", line)
        # Copy the iterable, as we can't reuse it later
        parts = list(parts_iterable)
        parts_found = [p.group() for p in parts]
        symbols_iterable = finditer("[^0-9\.]+", line)
        # Copy the iterable, as we can't reuse it later
        symbols = list(symbols_iterable)
        symbols_found = [s.group() for s in symbols]
        part_map = list()
        symbol_map = list()

        if len(parts_found) > 0:
            for part in parts:
                bpos = part.span()[0]
                epos = part.span()[1] - 1
                if bpos != 0:
                    # Adjacent could be left of position
                    bpos = bpos - 1
                if epos != LENGTH:
                    # Adjacent could be right of position
                    epos = epos + 1
                part_location = (part.group(), bpos, epos)
                part_map.append(part_location)
        engine_parts_map.append(part_map)

        symbol_location = None
        if len(symbols_found) > 0:
            for symbol in symbols:
                symbol_location = (symbol.group(), symbol.span()[0])
                symbol_map.append(symbol_location)
        engine_symbols_map.append(symbol_map)

    return (engine_parts_map, engine_symbols_map)


def sum_good_parts(parts_map, symbols_map) -> int:
    engine_map_length = len(parts_map) - 1
    line = 0
    good_parts = list()
    for parts in parts_map:
        if len(parts) > 0:
            if DEBUG:
                print(f"line {line+1} found parts : {parts}")
            for part in parts:
                good_part = False

                if len(symbols_map[line]) > 0:
                    # Test the symbols found on the same line for adjacency
                    for s in symbols_map[line]:
                        # Test if symbol is within bpos, epos
                        if s[1] >= part[1] and s[1] <= part[2]:
                            good_part = True
                            if DEBUG:
                                print(f" + good part {part[0]} near symbol ({s[0]}) on same line")

                if line >= 1 and len(symbols_map[line - 1]) > 0:
                    # Test the symbols found on the previous line for adjacency
                    for s in symbols_map[line - 1]:
                        # Test if symbol is within bpos, epos
                        if s[1] >= part[1] and s[1] <= part[2]:
                            good_part = True
                            if DEBUG:
                                print(f" + good part {part[0]} near symbol ({s[0]}) on previous line")

                if line < engine_map_length and len(symbols_map[line + 1]) > 0:
                    # Test the symbols found on the following line for adjacency
                    for s in symbols_map[line + 1]:
                        # Test if symbol is within bpos, epos
                        if s[1] >= part[1] and s[1] <= part[2]:
                            good_part = True
                            if DEBUG:
                                print(f" + good part {part[0]} near symbol ({s[0]}) on next line")

                if good_part:
                    good_parts.append(int(part[0]))

        line += 1
    return sum(good_parts)


if __name__ == "__main__":
    def example():
        test_parts_map, test_symbols_map = create_map(TEST)
        example_sum = sum_good_parts(test_parts_map, test_symbols_map)
        print(f"Sum of good engine parts (example): {example_sum}")
        assert example_sum == 4361

    def stage1():
        parts_map, symbols_map = create_map(read_url(URL))
        puzzle_sum = sum_good_parts(parts_map, symbols_map)
        print(f"Sum of good engine parts (puzzle): {puzzle_sum}")
        assert puzzle_sum > 294887

    DEBUG=False
    example()
    stage1()

