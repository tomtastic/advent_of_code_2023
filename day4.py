#!/usr/bin/env python3
import requests
from collections import deque

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
URL = "https://adventofcode.com/2023/day/4/input"
TEST = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def read_cookie(file: str) -> str:
    """Get the AdventOfCode session cookie we saved earlier"""
    with open(file, mode="r") as f:
        return f.read().strip()


def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""
    session_cookie = {"session": read_cookie(COOKIEFILE)}
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text


def phase1(input: str) -> int:
    scratchcards = list()
    for line in input.strip().split("\n"):
        _, info = [x.split(" | ") for x in line.split(": ")]
        # card_num = card[0].split(' ')[1]
        winning, chosen = [x.split() for x in info]
        points = 0
        for n in winning:
            if n in chosen and points == 0:
                points += 1
            elif n in chosen:
                points *= 2
        # print(f"{card_num} -> {winning} -> {chosen} == {points}")
        scratchcards.append(points)
    return sum(scratchcards)


def phase2(input: str) -> int:
    # First build a dict of all the scratchcards and their matched numbers
    t = dict()
    for line in input.strip().split("\n"):
        card, info = [x.split(" | ") for x in line.split(": ")]
        id = card[0].split()[1]
        winning, chosen = [x.split() for x in info]
        t[id] = {'winning': winning, 'chosen': chosen, 'matches': 0}
        for n in t[id]['winning']:
            if n in t[id]['chosen']:
                t[id]['matches'] += 1

    # Populate a double-ended queue with the contents of the dict
    queue: deque = deque()
    for n in t.keys():
        queue.append([n,t[str(n)]])

    card_tally = 0
    while len(queue) > 0:
        # Take off the front of the queue
        m = queue.popleft()
        card = m[0]
        info = m[1]
        if info['matches'] > 0:
            for copy in reversed(range(int(card)+1, int(card)+1+info['matches'])):
                #print(f"  + prepending card number {copy} on queue")
                queue.appendleft([copy,t[str(copy)]])
        card_tally += 1

    return card_tally

if __name__ == "__main__":
    print(f"Phase1 (example) : {phase1(TEST)}")
    print(f"Phase1           : {phase1(read_url(URL))}")
    print(f"Phase2 (example) : {phase2(TEST)}")
    print(f"Phase2           : {phase2(read_url(URL))}")
