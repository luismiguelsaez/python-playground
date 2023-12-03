import re, string
grid = [ list(l.rstrip()) for l in open('input.txt', 'r').readlines() ]

def find_adj(grid, point):
    points = filter(
        lambda x: x[0]>=0 and x[1]>=0 and x[0]<len(grid) and x[1]<len(grid[0]),
        [(point[0]+x, point[1]+y) for x in (-1,1,0) for y in (-1,1,0) if x != 0 or y != 0]
    )

    return points

def validate_part_num(grid, line, r):
    g = []
    c = []
    res = False
    symbols = set(string.punctuation.replace('.', ''))
    for i in range(r[0],r[1]):
        adj_coords = find_adj(grid, (line, i))
        for coord in adj_coords:
            c.append(grid[coord[0]][coord[1]])
            if grid[coord[0]][coord[1]] == '*':
                g.append(coord)
        if len((set(c)) & set(symbols)) > 0: res = True
    return res, set(g)

sum = 0
part_nums = []
part_gears = {}
for i in range(len(grid)):
    part_nums.append([])
    match = re.finditer('[0-9]+', ''.join(grid[i]))
    if match is not None:
        part_nums[i] = [(m.start(0), m.end(0)) for m in match]
        for j in part_nums[i]:
            valid, gears = validate_part_num(grid, i, j)
            print(f"[{i}] - {j} - {valid} - {gears}")
            if len(gears):
                for gear in gears:
                    if gear not in  part_gears:
                        part_gears[gear] = [int(''.join(grid[i][j[0]:j[1]]))]
                    else:
                        part_gears[gear].append(int(''.join(grid[i][j[0]:j[1]])))
            if valid:
                sum += int(''.join(grid[i][j[0]:j[1]]))

print(f"Part one: {sum}")

gear_ratios_sum = 0
for gear in part_gears:
    gear_ratio = 0
    if len(part_gears[gear]) == 2:
        gear_ratio = part_gears[gear][0] * part_gears[gear][1]
        gear_ratios_sum += gear_ratio
        #print(f"Gear {gear} - {part_gears[gear]} - {gear_ratio}")

print(f"Part two: {gear_ratios_sum}")
