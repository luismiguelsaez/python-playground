
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
