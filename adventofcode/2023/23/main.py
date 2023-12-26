from sys import argv
from time import sleep
import copy

grid = [list(l.rstrip()) for l in open(argv[1], 'r').readlines()]

class Node():
    def __init__(self, coord, parent):
        self.coord = coord
        self.parent = parent

class Map():
    symbols = {
        'v': (1, 0),
        '^': (-1, 0),
        '<': (0, -1),
        '>': (0, 1)
    }

    def __init__(self, grid, start, visited=[]):
        self.grid = grid
        self.start = start
        self.aux_grid = copy.deepcopy(grid)
        self.visited = visited
        self.path_lenghts = []
    
    def print_map(self):
        print("\033c")
        for r in self.grid: print(*r, sep='')
    
    def print_aux(self):
        for r in self.aux_grid: print(*r, sep='')

    def dfs(self):
        heap = list()
        self.visited = list()
        
        heap.append(self.start)
        
        while len(heap) > 0:
            cur = heap.pop()
            self.visited.append(cur)
            self.aux_grid[cur[0]][cur[1]] = 'O'

            if cur[0] == len(grid) - 1:
                break
            
            neighbors = [ 
                            (cur[0]+x, cur[1]+y) for x, y in [(0, 1), (1, 0), (0, -1), (-1, 0)]
                            if 0 <= cur[0]+x < len(grid) and 0 <= cur[1]+y < len(grid[0]) and grid[cur[0]+x][cur[1]+y] != '#'
                        ]

            cross_count = 0
            cross_alts = []
            for n in neighbors:
                if n not in self.visited:
                    if grid[n[0]][n[1]] == '.':
                        heap.append((n[0], n[1]))
                        self.aux_grid[n[0]][n[1]] = 'O'
                    else:
                        symbol = grid[n[0]][n[1]]
                        dir_to_slope = ( n[0] - cur[0], n[1] - cur[1] )
                        slope_dir = self.symbols[symbol]
                        if ( dir_to_slope[0] + slope_dir[0], dir_to_slope[1] + slope_dir[1]) != (0 ,0):
                            next = (n[0] + self.symbols[symbol][0], n[1] + self.symbols[symbol][1])
                            cross_count += 1
                            cross_alts.append((n, next))
                        else:
                            pass

            if cross_count > 0:
                alt_length_max = -1
                alt_max = None
                s_max = None
                for s, alt in cross_alts:
                    alt_length = Map(self.grid, alt, self.visited).dfs()
                    if alt_length > alt_length_max:
                        alt_max = alt
                        s_max = s
                        alt_length_max = alt_length
                self.visited.append(s_max)
                heap.append(alt_max)

        return len(set(self.visited))

m = Map(grid, (0, 1))
print(m.dfs())
m.print_aux()
