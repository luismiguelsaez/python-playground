from requests import get

# Get session cookie after login to adventofcode.com
session = '53616c7465645f5f2596cddc32bc251ebdc3b21070bbf3af3f2bd32ac8054d7793c9a0bf8affc014c500bff2c2e337c5dcc62093649140fb38d28f4a8795f288'
res = get('https://adventofcode.com/2022/day/4/input', cookies={'session': session})
input = res.text

assignments = input.split('\n')

count = 0
count_total = 0
for a in assignments:
  if a != '':
    splitted = a.split(',')
    first_ini = int(splitted[0].split('-')[0])
    first_end = int(splitted[0].split('-')[1])
    second_ini = int(splitted[1].split('-')[0])
    second_end = int(splitted[1].split('-')[1])
    
    if (first_ini >= second_ini and first_end <= second_end):
      print(f"{splitted[0]} fits in {splitted[1]}")
      count += 1
    elif (second_ini >= first_ini and second_end <= first_end):
      print(f"{splitted[1]} fits in {splitted[0]}")
      count += 1
    
    count_total += 1

# First part 
print(count_total, count)


count = 0

for a in assignments:
  if a != '':
    splitted = a.split(',')
    first_ini = int(splitted[0].split('-')[0])
    first_end = int(splitted[0].split('-')[1])
    second_ini = int(splitted[1].split('-')[0])
    second_end = int(splitted[1].split('-')[1])
    
    if (first_ini >= second_ini and first_end <= second_end):
      print(f"{splitted[0]} fits in {splitted[1]}")
      count += 1
    elif (second_ini >= first_ini and second_end <= first_end):
      print(f"{splitted[1]} fits in {splitted[0]}")
      count += 1
    else:
      if set(range(first_ini, first_end + 1)) & set(range(second_ini, second_end + 1)):
        print(f"Overlapping {splitted[0]} and {splitted[1]}")
        count += 1

# Second part 
print("Overlapping total", count)

