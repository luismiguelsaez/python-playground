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

nums_conv = {
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

nums = ['1','2','3','4','5','6','7','8','9',
        'one','two','three','four','five','six','seven','eight','nine']

def get_digits(line: str):
    regex_str = f"({'|'.join(nums)})"
    matches = []
    for n in nums:
        res = re.finditer(n, line)
        for i in res:
            matches.append(i.span())
    matches.sort(key=lambda n: n[0])

    digits = []
    for m in matches:
        digit = line[m[0]:m[1]]
        if digit.isdigit():
            digits.append(digit)
        else:
            digits.append(nums_conv[digit])
    return digits

sum = 0
c = 0
for line in lines:
    orig = line
    digits = get_digits(line)
    first = ""
    last = ""
    num = ""
    for char in digits:
        if first == "":
            first = char
        last = char
    num = first + last
    sum += int(num)
    c += 1

print(f"Part two: {sum}")
