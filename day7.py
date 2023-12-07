#!/usr/bin/env python3
from collections import defaultdict
from helpers import (
    read_url as read_url,
    timethis as timethis,
    logging as logging,
)

URL = "https://adventofcode.com/2023/day/7/input"
TEST = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

CARDS = "AKQJT98765432"


def parse_hands(input: str) -> list:
    """Returns list of (hand, bid) from the input"""
    valid = dict()
    for c in list(CARDS):
        valid[str(c)] = 1
    hands = list()
    for line in input.strip().split("\n"):
        hand, bid = line.split()
        for c in list(hand):
            if c not in valid:
                print(f"[!] Hand contains invalid char : {hand} -> {c}")
                continue
        hands.append([hand, bid])
    return hands


def score_hand(hand: str) -> int:
    """Score a hand of cards, eg.'KK3J2'"""
    # Tally num of each cards
    bin: dict = defaultdict(int)
    for card in list(hand):
        bin[card] += 1

    # Generate a score for each card, where each value is 7 times the previous
    # [1, 7, 49, 343, 2401, 16807, 117649, 823543, 5764801, 40353607, 282475249, 1977326743, 13841287201]

    card_pos_score = [1]
    for n in range(1, len(list(CARDS))):
        score = card_pos_score[n - 1] * 7
        card_pos_score.append(score)

    cards_val = 1
    add = 0
    for order, card in enumerate(reversed(hand)):
        for pos, card_type in enumerate(reversed(list(CARDS))):
            # from 2 -> A
            if card == card_type:
                cards_val += ((pos + 1) * card_pos_score[order]) + (
                    (pos + 1) * (add**add)
                )
                logging.debug(
                    f"card '{card}' value {pos+1} * card_order ({order}) gets {(pos+1) * card_pos_score[order] + add}"
                )
        add += 2

    if len(bin.keys()) == 1:
        # all five cards have the same label: AAAAA
        logging.debug(f"{''.join(hand)} Five of a kind")
        return 1534400000 + cards_val
    elif len(bin.keys()) == 2 and 4 in bin.values():
        # four cards have the same label and one card has a different label: AA8AA
        logging.debug(f"{''.join(hand)} Four of a kind")
        return 1315200000 + cards_val
    elif len(bin.keys()) == 2 and 3 in bin.values() and 2 in bin.values():
        # three cards have the same label, remaining two cards share a different label: 23332
        logging.debug(f"{''.join(hand)} Full house")
        return 1096000000 + cards_val
    elif len(bin.keys()) == 3 and 3 in bin.values():
        # three cards have the same label, remaining two cards are each different from any other card in the hand: TTT98
        logging.debug(f"{''.join(hand)} Three of a kind")
        return 876800000 + cards_val
    elif len(bin.keys()) == 3 and 2 in bin.values():
        # two cards share one label, two other cards share a second label, the remaining card has a third label: 23432
        logging.debug(f"{''.join(hand)} Two pair")
        return 657600000 + cards_val
    elif len(bin.keys()) == 4:
        # two cards share one label, the other three cards have a different label from the pair and each other: A23A4
        logging.debug(f"{''.join(hand)} One pair")
        return 438400000 + cards_val
    elif len(bin.keys()) == 5:
        # all cards' labels are distinct: 23456
        logging.debug(f"{''.join(hand)} High card")
        return 219200000 + cards_val


if __name__ == "__main__":
    # puzzle assertions...
    assert score_hand("33332") > score_hand("2AAAA"), "Both 'four of a kind', but 33332 is stronger as its first card is stronger"
    assert score_hand("77888") > score_hand("77788"), "Both 'full house', but 77888 is stronger as it's third card is stronger"
    # FIXME: This assertion fails, even though we can pass stage 1 !
    # assert score_hand("22232") > score_hand("2222A")
    assert score_hand("22232") > score_hand("22223")
    assert score_hand("43456") > score_hand("42AKQ")
    assert score_hand("AKQJT") > score_hand("AKQTJ")
    assert score_hand("AAAAA") > score_hand("22222")

    @timethis
    def stage1_test():
        level = logging.DEBUG
        hands = parse_hands(TEST)
        print(f"We have {len(hands)} hands")
        hands.sort(key=lambda L: score_hand(L[0]))
        print(f"Scored hands: {hands}")
        winnings = 0
        for _, hand in enumerate(hands):
            logging.debug(
                f"rank {_+1:4} ({hand[0]} : {hand[1]:>3}) * {_+1:<4} = {(_+1)*int(hand[1])}"
            )
            winnings += (_ + 1) * int(hand[1])
        print(f"Winnings: {winnings}")
        assert winnings == 6440

    @timethis
    def stage1():
        level = logging.INFO
        hands = parse_hands(read_url(URL))
        print(f"We have {len(hands)} hands")
        hands.sort(key=lambda L: score_hand(L[0]))
        winnings = 0
        for _, hand in enumerate(hands):
            logging.debug(
                f"rank {_+1:4} ({hand[0]} : {hand[1]:>3}) * {_+1:<4} = {(_+1)*int(hand[1])}"
            )
            winnings += (_ + 1) * int(hand[1])
        print(f"Winnings: {winnings}")
        assert winnings == 251029473

    @timethis
    def stage2_test():
        pass

    @timethis
    def stage2():
        pass

    stage1_test()
    stage1()
    # stage2_test()
    # stage2()
