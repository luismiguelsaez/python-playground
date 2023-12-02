import re

with open('input.txt', 'r') as f:
    lines = [ l.rstrip() for l in f.readlines() ]

threshold = {'red':12,'green': 13,'blue': 14}

sum = 0
power_sum = 0
for line in lines:
    color_max = {'red': 0,'green': 0,'blue': 0}
    match_game = re.search('^Game ([0-9]+): (.*)', line)
    game = match_game.groups()[0]
    reveals = match_game.groups()[1]

    print(f"- {game} - {line}")
    game_wrong = False
    for reveal in reveals.split('; '):
        for set in reveal.split(', '):
            set_wrong = False
            num, color = (set.split(' '))
            if color_max[color] < int(num):
                color_max[color] = int(num)
            if int(num) > threshold[color]:
                set_wrong = True
                game_wrong = True
    if not game_wrong:
        sum += int(game)
    line_power = color_max['red'] * color_max['green'] * color_max['blue']
    power_sum += line_power
    print(f" - {color_max} - {line_power}")

print(f"Part one: {sum}")
print(f"Part two: {power_sum}")
