#!/usr/bin/env python3
import requests

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
URL = "https://adventofcode.com/2023/day/2/input"

def read_cookie(file: str) -> str:
    """Get the AdventOfCode session cookie we saved earlier"""
    with open(file, mode="r") as f:
        return f.read().strip()

def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""
    session_cookie = { 'session': read_cookie(COOKIEFILE) }
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text


if __name__ == "__main__":
    input = (read_url(URL))

    for line in input.split():
        print(f"{line}")
