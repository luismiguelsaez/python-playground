from requests import get

# Get session cookie after login to adventofcode.com
session = '53616c7465645f5f2596cddc32bc251ebdc3b21070bbf3af3f2bd32ac8054d7793c9a0bf8affc014c500bff2c2e337c5dcc62093649140fb38d28f4a8795f288'
res = get('https://adventofcode.com/2022/day/2/input', cookies={'session': session})
input = res.text

mean = {
  'A': 'rock',
  'B': 'paper',
  'C': 'scissors',
  'X': 'rock',
  'Y': 'paper',
  'Z': 'scissors'
}

wins = {
  'A': 'Y',
  'B': 'Z',
  'C': 'X'
}

loss = {
  'A': 'Z',
  'B': 'X',
  'C': 'Y'
}

draw = {
  'A': 'X',
  'B': 'Y',
  'C': 'Z'
}

scores = {
  'X': 1,
  'Y': 2,
  'Z': 3
}

total = 0
for line in input.split('\n'):
  if line != '':
    score = 0
    op = line[0]
    me = line[2]
    if wins[op] == me:
      score = 6 + scores[me]
    elif loss[op] == me:
      score = scores[me]
    else:
      score = 3 + scores[me]
    total += score

# First part
print(f"Total points (1): {total}")

total = 0
for line in input.split('\n'):
  if line != '':
    score = 0
    op = line[0]
    res = line[2]
    if res == 'X':
      score = scores[loss[op]]
    elif res == 'Y':
      score = 3 + scores[draw[op]]
    else:
      score = 6 + scores[wins[op]]
    total += score

# Second part
print(f"Total points (2): {total}")
