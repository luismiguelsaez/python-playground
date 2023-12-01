import re

with open('input.txt', 'r') as f:
    lines = [ l.rstrip() for l in f.readlines() ]

sum = 0
for line in lines:
    first = ""
    last = ""
    num = ""
    for char in line:
        if char.isdigit():
            if first == "":
                first = char
            last = char
    num = first + last
    sum += int(num)

print(f"Part one: {sum}")

with open('input.txt', 'r') as f:
    lines = [ l.rstrip() for l in f.readlines() ]

nums = {
    'nine':  '9',
    'eight': '8',
    'seven': '7',
    'six':   '6',
    'five':  '5',
    'four':  '4',
    'three': '3',
    'two':   '2',
    'one':   '1'
}

def replace_nums(line: str)->str:
    words = re.findall("(one|two|three|four|five|six|seven|eight|nine)", line)
    for word in words:
        line = line.replace(word, nums[word], 1)
    return line

sum = 0
for line in lines:
    orig = line
    line = replace_nums(line)
    first = ""
    last = ""
    num = ""
    for char in line:
        if char.isdigit():
            if first == "":
                first = char
            last = char
    num = first + last
    sum += int(num)
    print(f"{orig} - {line} - {first} - {last} - {num} - {sum}")

print(f"Part two: {sum}")
