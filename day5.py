#!/usr/bin/env python3
from helpers import timethis as timethis, read_url as read_url
import re

URL = "https://adventofcode.com/2023/day/5/input"
TEST = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""


def read_almanac_stage1(input: str) -> dict:
    """Take the input string and build a dict of seeds and maps"""
    """Refactored for speed and efficiency"""
    almanac = dict()
    map_token = None
    for line in input.strip().split("\n"):
        if re.match("^$", line):
            # Clear the map token if we encounter a blank line
            map_token = None
        elif re.findall("seeds:", line):
            # The list of seeds
            almanac["seeds"] = line.strip().split()[1:]
        elif re.findall("map:", line):
            # A map token
            map_token = line.split()[0]
            almanac[map_token] = list()
        elif map_token and re.findall("^[0-9]", line):
            # We must be reading mapping data, so add to the list of ranges
            map_data = line.split()
            almanac[map_token].append(decode_map(map_data))
        else:
            print(f"unknown line type: {line}")
    return almanac


def decode_map(ranges: list) -> dict:
    """Returns dict of source to destination [start, end] mappings"""
    dst_start, src_start, range_length = ranges
    return {
        "src": [int(src_start), int(src_start) + int(range_length)],
        "dst": [int(dst_start), int(dst_start) + int(range_length)],
    }


def read_almanac_stage2(input: str) -> dict:
    """Take the input string and build a dict of seeds and maps"""
    """Refactored for speed and efficiency"""
    almanac = dict()
    map_token = None
    for line in input.strip().split("\n"):
        if re.match("^$", line):
            # Clear the map token if we encounter a blank line
            map_token = None
        elif re.findall("seeds:", line):
            # The range of seeds
            almanac["seeds"] = list()
            all_seeds = iter(line.strip().split()[1:])
            for x in all_seeds:
                almanac["seeds"].append([x, next(all_seeds)])
        elif re.findall("map:", line):
            # A map token
            map_token = line.split()[0]
            almanac[map_token] = list()
        elif map_token and re.findall("^[0-9]", line):
            # We must be reading mapping data, so add to the list of ranges
            map_data = line.split()
            almanac[map_token].append(decode_map(map_data))
        else:
            print(f"unknown line type: {line}")

    return almanac


# Very hot path
def get_mapping(almanac: dict, source: int, map: str) -> int:
    """Return the mapping if found, or source if not"""
    # mapping['src|dst'] = [ start, end ]
    for mapping in almanac[map]:
        if source >= mapping["src"][0] and source <= mapping["src"][1]:
            return mapping["dst"][0] + source - mapping["src"][0]
    # If no match, then destination is source
    return source


# Very hot path
def seed_to_location(almanac: dict, seed: int) -> int:
    """Walk the maps from seed and return the location"""
    soil = get_mapping(almanac, seed, "seed-to-soil")
    fertilizer = get_mapping(almanac, soil, "soil-to-fertilizer")
    water = get_mapping(almanac, fertilizer, "fertilizer-to-water")
    light = get_mapping(almanac, water, "water-to-light")
    temperature = get_mapping(almanac, light, "light-to-temperature")
    humidity = get_mapping(almanac, temperature, "temperature-to-humidity")
    return get_mapping(almanac, humidity, "humidity-to-location")


if __name__ == "__main__":

    def stage1_test():
        almanac = read_almanac_stage1(TEST)
        lowest_location = min(
            [seed_to_location(almanac, int(x)) for x in almanac["seeds"]]
        )
        print(f"{'Stage1 example':16} : {lowest_location}")

    def stage1():
        almanac = read_almanac_stage1(read_url(URL))
        lowest_location = min(
            [seed_to_location(almanac, int(x)) for x in almanac["seeds"]]
        )
        print(f"{'Stage1':16} : {lowest_location}")

    def stage2_test():
        """A small test range, lets do it in one"""
        almanac = read_almanac_stage2(TEST)
        large_range = list()
        for pair in almanac["seeds"]:
            large_range.extend(list(range(int(pair[0]), int(pair[0]) + int(pair[1]))))
        lowest_location = min([seed_to_location(almanac, int(x)) for x in large_range])
        print(f"{'Stage2 example':16} : {lowest_location}")

    @timethis
    def stage2():
        """A huge test range, iterate over seed pairs to see progress"""
        almanac = read_almanac_stage2(read_url(URL))

        def _optimise_almanac_ranges(_almanac) -> dict:
            """To avoid iterating over many mapping ranges in a very"""
            """hot part of the code, we notice the actual puzzle ranges"""
            """are contiguous so we can coalesce them into a single range"""
            for map_token in _almanac:
                if map_token == "seeds":
                    # skip this non-map key
                    continue
                src_range_list = list()
                dst_range_list = list()
                for ranges in _almanac[map_token]:
                    src_range_list.append((ranges["src"][0], ranges["src"][1]))
                src_min = min(src_range_list)[0]
                src_max = max(src_range_list)[1]
                for ranges in _almanac[map_token]:
                    dst_range_list.append((ranges["dst"][0], ranges["dst"][1]))
                dst_min = min(dst_range_list)[0]
                dst_max = max(dst_range_list)[1]
                _almanac[map_token] = [
                    {
                        "src": [src_min, src_max],
                        "dst": [dst_min, dst_max],
                    }
                ]
            return _almanac

        almanac = _optimise_almanac_ranges(almanac)

        location = 99999999999
        for pair in almanac["seeds"]:
            print(f"Checking seed pairs : {pair}", flush=True)
            for seed in range(int(pair[0]), int(pair[0]) + int(pair[1])):
                new_location = seed_to_location(almanac, seed)
                if new_location < location:
                    print(f" - new lowest location: {new_location}", flush=True)
                    location = new_location
        print(f"{'Stage2':16} : {location}")

    stage1_test()
    stage1()
    stage2_test()
    stage2()
