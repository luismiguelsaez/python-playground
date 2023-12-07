from sys import argv
import collections

lines = [l.rstrip() for l in open(argv[1], 'r').readlines()]

table = {}
for l in range(len(lines)):
    hand, bid = lines[l].split(' ')
    char_count = list(filter(lambda x:x[1] > 1, collections.Counter(hand).items()))
    kind_count = sorted(list(collections.Counter([i[1] for i in char_count]).items()), reverse=True)
    strength = 0
    match kind_count:
        case [(5, 1)]:         strength = 6
        case [(4, 1)]:         strength = 5
        case [(3, 1), (2, 1)]: strength = 4
        case [(3, 1)]:         strength = 3
        case [(2, 2)]:         strength = 2
        case [(2, 1)]:         strength = 1
        case []:               strength = 0
    table[hand] = {}
    table[hand]['bid'] = bid
    table[hand]['strength'] = strength

items = []
for item in table:
    items.append(table[item] | {"val": item})

labels = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

c = 1
while c <= len(items):
    for item in range(len(items) - c ):
        if items[item]['strength'] < items[item + 1]['strength']:
            items[item], items[item + 1] = items[item + 1], items[item]
        if items[item]['strength'] == items[item + 1]['strength']:
            for i,j in zip(list(items[item]['val']), list(items[item + 1]['val'])):
                if labels.index(i) < labels.index(j):
                    break
                if labels.index(i) > labels.index(j):
                    items[item], items[item + 1] = items[item + 1], items[item]
                    break
    c += 1

sum = 0
for i in range(len(items)):
    sum += (len(items) - i) * int(items[i]['bid'])

print(f"Part one: {sum}")


table = {}
for l in range(len(lines)):
    hand, bid = lines[l].split(' ')
    char_count = list(filter(lambda x:x[1] > 1, collections.Counter(hand).items()))
    kind_count = sorted(list(collections.Counter([i[1] for i in char_count]).items()), reverse=True)
    strength = 0
    match kind_count:
        case [(5, 1)]:         strength = 6
        case [(4, 1)]:         strength = 5 if collections.Counter(hand)['J'] == 0 else (6 if collections.Counter(hand)['J'] in (1, 4) else 0)
        case [(3, 1), (2, 1)]: strength = 4 if collections.Counter(hand)['J'] == 0 else (6 if collections.Counter(hand)['J'] in (2, 3) else (5 if collections.Counter(hand)['J'] == 1 else 0))
        case [(3, 1)]:         strength = 3 if collections.Counter(hand)['J'] == 0 else (5 if collections.Counter(hand)['J'] == 3 else (5 if collections.Counter(hand)['J'] == 1 else 0))
        case [(2, 2)]:         strength = 2 if collections.Counter(hand)['J'] == 0 else (4 if collections.Counter(hand)['J'] == 1 else (5 if collections.Counter(hand)['J'] == 2 else 0))
        case [(2, 1)]:         strength = 1 if collections.Counter(hand)['J'] == 0 else (3 if collections.Counter(hand)['J'] in (1, 2) else 0)
        case []:               strength = 0 if collections.Counter(hand)['J'] == 0 else (1 if collections.Counter(hand)['J'] == 1 else 0)
    table[hand] = {}
    table[hand]['bid'] = bid
    table[hand]['strength'] = strength

items = []
for item in table:
    items.append(table[item] | {"val": item})

labels = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

c = 1
while c <= len(items):
    for item in range(len(items) - c ):
        if items[item]['strength'] < items[item + 1]['strength']:
            items[item], items[item + 1] = items[item + 1], items[item]
        if items[item]['strength'] == items[item + 1]['strength']:
            for i,j in zip(list(items[item]['val']), list(items[item + 1]['val'])):
                if labels.index(i) < labels.index(j):
                    break
                if labels.index(i) > labels.index(j):
                    items[item], items[item + 1] = items[item + 1], items[item]
                    break
    c += 1

sum = 0
for i in range(len(items)):
    sum += (len(items) - i) * int(items[i]['bid'])

print(f"Part two: {sum}")
#print(items)