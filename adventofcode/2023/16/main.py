from sys import argv
from time import sleep
import copy

grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

class Point():
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent

def calc_beams(s = Point((0, 0), (0, -1))):
    grid_draw = copy.deepcopy(grid)
    visited = [(s.coord, ())]
    queue = [s]
    grid_draw[s.coord[0]][s.coord[1]] = '#'
    while len(queue) > 0:
        c = queue.pop()
        d = ( c.coord[0] - c.parent[0], c.coord[1] - c.parent[1])
        match grid[c.coord[0]][c.coord[1]]:
            case '|':
                if d[1] in [1, -1]:
                    n = [Point( (c.coord[0] + y, c.coord[1]), c.coord) for y in [-1, 1] if len(grid) > c.coord[0] + y >= 0]
                else:
                    n = [Point( (c.coord[0] + d[0], c.coord[1] + d[1]), c.coord )] if len(grid) > c.coord[0] + d[0] >= 0 else []
            case '-':
                if d[0] in [1, -1]:
                    # TO FIX - out of bounds
                    n = [Point( (c.coord[0], c.coord[1] + x), c.coord ) for x in [-1, 1] if len(grid[0]) > c.coord[1] + x >= 0]
                else:
                    n = [Point( (c.coord[0] + d[0], c.coord[1] + d[1]), c.coord ) ] if len(grid[0]) > c.coord[1] + d[1] >= 0 else []
            case '/':
                if d[1] == 1:
                    n = [Point( (c.coord[0] - 1, c.coord[1]), c.coord )] if c.coord[0] - 1 >= 0 else []
                if d[1] == -1:
                    n = [Point( (c.coord[0] + 1, c.coord[1]), c.coord )] if len(grid) > c.coord[0] + 1 else []
                if d[0] == 1:
                    n = [Point( (c.coord[0], c.coord[1] - 1), c.coord )] if c.coord[1] - 1 >= 0 else []
                if d[0] == -1:
                    n = [Point( (c.coord[0], c.coord[1] + 1), c.coord )] if len(grid[0]) > c.coord[1] + 1 else []
            case '\\':
                if d[1] == 1:
                    n = [Point( (c.coord[0] + 1, c.coord[1]), c.coord )] if len(grid) > c.coord[0] + 1 else []
                if d[1] == -1:
                    n = [Point( (c.coord[0] - 1, c.coord[1]), c.coord )] if c.coord[0] - 1 >= 0 else []
                if d[0] == 1:
                    n = [Point( (c.coord[0], c.coord[1] + 1), c.coord )] if len(grid[0]) > c.coord[1] + 1 else []
                if d[0] == -1:
                    n = [Point( (c.coord[0], c.coord[1] - 1), c.coord )] if c.coord[1] - 1 >= 0 else []
            case '.':
                if ( len(grid[0]) > (c.coord[1] + d[1]) >= 0 ) and ( len(grid) > (c.coord[0] + d[0]) >= 0 ):
                    n = [Point( (c.coord[0] + d[0], c.coord[1] + d[1]), c.coord )]
                else:
                    n = []

        for np in n:
            if (c.coord, c.parent) not in visited:
                queue.insert(0, np)
        visited.append((c.coord, c.parent))

        # Print
        grid_draw[c.coord[0]][c.coord[1]] = '#'

    energized = 0
    for r in range(len(grid_draw)):
        for c in range(len(grid_draw[r])):
            if grid_draw[r][c] == '#':
                energized += 1

    return energized

print(f"Part one: {calc_beams(Point((0, 0), (0, -1)))}")


starts = []
for c in range(len(grid[0])):
    starts.append(Point((len(grid) - 1, c), (len(grid), c)))
    starts.append(Point((0, c), (-1, c)))

for r in range(len(grid)):
    starts.append(Point((r, len(grid[r]) - 1), (r, len(grid[r]))))
    starts.append(Point((r, 0), (r, -1)))

res = []
for s in starts:
    res.append(calc_beams(s))

print(f"Part two: {max(res)}")
