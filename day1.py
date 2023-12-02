#!/usr/bin/env python3
import requests
import regex

# Session cookie is valid for 10 years!
COOKIEFILE = ".session_cookie"
URL = "https://adventofcode.com/2023/day/1/input"
NUMS = ['zero','one','two','three','four','five','six','seven','eight','nine']

def read_cookie(file: str) -> str:
    """Get the AdventOfCode session cookie we saved earlier"""
    with open(file, mode="r") as f:
        return f.read().strip()

def read_url(url: str) -> str:
    """Get the unmolested data from a URL"""
    session_cookie = { 'session': read_cookie(COOKIEFILE) }
    with requests.get(url=url, timeout=5, cookies=session_cookie) as content:
        return content.text

def numwords_to_nums(input: str) -> str:
    for numword in NUMS:
        if numword in input:
            input = input.replace(numword, str(NUMS.index(numword)))
    return input

def split_on_window(sequence, limit=5) -> list:
    """Split a contiguous string into list of window lengths"""
    if len(sequence) < limit:
        # No windowing possible at this length
        return [sequence]
    results = []
    split_sequence = "".join(list(sequence))
    iteration_length = len(split_sequence) - (limit - 1)
    max_window_indicies = range(iteration_length)
    for index in max_window_indicies:
        results.append(split_sequence[index:index + limit])
    return results

def get_calibration_value_stage1(text: str) -> int:
    digits = regex.findall('[0-9]{1}', text)

    if len(digits) == 1:
        # A special case, repeat the single matched digit
        return(int(digits[0] + digits[0]))
    else:
        # Otherwise, first and last digit
        return(int(digits[0] + digits[-1]))

def get_calibration_value_stage2(text: str) -> int:
    # Because we only care about the first and last digits in the string,
    # we can convert each and every window size chunk
    new_text = ""
    for window in split_on_window(text):
        new_text += numwords_to_nums(window)

    digits = regex.findall('[0-9]{1}', new_text)

    if len(digits) == 1:
        # A special case, repeat the single matched digit
        return(int(digits[0] + digits[0]))
    else:
        # Otherwise, first and last digit
        return(int(digits[0] + digits[-1]))


if __name__ == "__main__":
    input = (read_url(URL))

    sum = 0
    for line in input.split():
        calibration_value = get_calibration_value_stage1(line)
        sum += calibration_value
    print(f"Sum of all calibration_values (stage1) = {sum}")

    sum = 0
    for line in input.split():
        calibration_value = get_calibration_value_stage2(line)
        sum += calibration_value
    print(f"Sum of all calibration_values (stage2) = {sum}")
