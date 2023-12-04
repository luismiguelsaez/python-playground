import re

def get_points(num: int):
    sum = 0
    for i in range(num):
        if i == 0:
            sum = 1
        else:
            sum = sum * 2
    return sum

lines = [ l.rstrip() for l in open('input.txt', 'r').readlines() ]

cards = {}
for line in lines:
    match_card = re.search('^Card\\s+([0-9]+):\\s+(.*)', line)
    card, nums = (match_card.groups())
    card_values = {'nums': nums, 'count': 1}
    cards[int(card)] = card_values

total_points = 0
for card in cards:
    card, nums = card, cards[card]['nums']
    #print(f"-- Card {card} -- {nums}")
    bet, win = nums.split('|')
    match_bets = re.finditer('[0-9]+', bet)
    bets, wins = [], []
    if match_bets is not None:
        bets = [bet[m.start(0):m.end(0)] for m in match_bets]
    match_wins = re.finditer('[0-9]+', win)
    if match_wins is not None:
        wins = [win[m.start(0):m.end(0)] for m in match_wins]
    #print(f"  - Bets: {bets} Wins: {wins}")
    matches = 0
    for b in bets:
        if b in wins:
            matches += 1
    for i in range(card + 1, card + 1 + matches):
        cards[i]['count'] += ( cards[card]['count'] ) * matches / len(range(card + 1, card + 1 + matches))
    points = get_points(matches)
    total_points += points
    #print(f"  - Matches: {matches} - {points} - increase {[i for i in range(card + 1, card + 1 + matches)]}")

#print(cards)

print(f"Part one: {total_points}")

total_scratchcards = 0
for card in cards:
    total_scratchcards += cards[card]['count']

print(f"Part two: {int(total_scratchcards)}")
