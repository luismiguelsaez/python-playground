from requests import get

# Get session cookie after login to adventofcode.com
session = '53616c7465645f5f2596cddc32bc251ebdc3b21070bbf3af3f2bd32ac8054d7793c9a0bf8affc014c500bff2c2e337c5dcc62093649140fb38d28f4a8795f288'
res = get('https://adventofcode.com/2022/day/1/input', cookies={'session': session})
input = res.text

sum = 0
max = 0
count = 0
elves = []
for line in input.split('\n'):
  if line == '':
    if sum > max:
      max = sum
    elves.append(sum)
    sum = 0
  else:
    sum += int(line)
  count += 1

top_3_elves = sorted(elves, reverse=True)[:3]

total = 0
for i in top_3_elves:
  total += i

# First part
print(f"The elf carrying most calories: {max}")

# Second part
print(f"Sum of top 3 elves: {total}")
