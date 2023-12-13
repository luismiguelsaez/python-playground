from sys import argv

lines = [l.rstrip() for l in open(argv[1], 'r').readlines()]

def scan(grid):
    total = 0
    for r in range(0, len(grid) - 1):
        if grid[r] == grid[r + 1]:
            u, d = r, r + 1
            while u > 0 and d < len(grid) - 1 and grid[u] == grid[d]:
                u, d = u - 1, d + 1
            if grid[u] == grid[d]:
                total += r + 1
    return total

def scan_replace(grid):
    for repeat in range(2):
        total = 0
        for r in range(0, len(grid) - 1):
            if grid[r] == grid[r + 1]:
                u, d = r, r + 1
                while u > 0 and d < len(grid) - 1 and grid[u] == grid[d]:
                    u, d = u - 1, d + 1
                if grid[u] == grid[d]:
                    total += r + 1
                else:
                    if repeat == 0:
                        diff = [i for i in range(len(grid[u])) if grid[u][i] != grid[d][i]]
                        idx = diff[0]
                        print(f"Set grid rows {u} and {d} to '.' at index {idx}")
                        grid[u][idx] = '.'
                        grid[d][idx] = '.'

    return total

def grid_process(grid):
    total_horizontal = 0
    total_vertical = 0

    total_horizontal = scan(grid) * 100

    columns = [[ grid[r][c] for r in range(len(grid) - 1, -1, -1) ] for c in range(len(grid[0]))]

    total_vertical = scan(columns)

    return total_horizontal + total_vertical

def grid_process_replace(grid):
    total_horizontal = 0
    total_vertical = 0

    total_horizontal = scan_replace(grid) * 100

    columns = [[ grid[r][c] for r in range(len(grid) - 1, -1, -1) ] for c in range(len(grid[0]))]

    total_vertical = scan_replace(columns)

    return total_horizontal + total_vertical

grid = []
results = []
for l in range(len(lines)):
    if lines[l] != '':
        grid.append(list(lines[l]))
    else:
        results.append(grid_process(grid))
        grid = []

results.append(grid_process(grid))

print(f"Part one: {sum(results)}")

grid = []
results = []
for l in range(len(lines)):
    if lines[l] != '':
        grid.append(list(lines[l]))
    else:
        results.append(grid_process_replace(grid))
        grid = []

results.append(grid_process_replace(grid))

print(f"Part two: {sum(results)}")
