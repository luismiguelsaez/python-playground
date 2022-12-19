from time import sleep


grid = [['.' for _ in range(20)] for _ in range(20)]

def print_grid(g: list)->None:
  for l in g:
    print(*l)

def update_grid(g: list, c_pos: tuple, p_pos: tuple, c: str)->list:
  g[c_pos[0]][c_pos[1]] = c
  g[p_pos[0]][p_pos[1]] = '.'
  return g

def check_touch(c_pos: tuple, p_pos: tuple)->bool:
  if p_pos not in [ (c_pos[0]+1, c_pos[1]),(c_pos[0]-1, c_pos[1]),(c_pos[0], c_pos[1]+1),(c_pos[0], c_pos[1]-1),
                    (c_pos[0]+1, c_pos[1]+1),(c_pos[0]-1, c_pos[1]-1),(c_pos[0]-1, c_pos[1]+1),(c_pos[0]+1, c_pos[1]-1),
                    c_pos ]:
    #print(f"{c_pos} not touching {p_pos}")
    return False
  else:
    return True

ph = 0
pt = 0
start_pos = (10, 10)
positions_h = []
positions_h.append(start_pos)
positions_t = []
positions_t.append(start_pos)

grid[start_pos[0]][start_pos[1]] = 'T'
grid[start_pos[0]][start_pos[1]] = 'H'

with open('input.txt') as file:
  lines = file.readlines()
  for i in range(len(lines)):
    dir = lines[i].strip()[0:1]
    num = int(lines[i].strip()[1:])
    for i in range(num):
      if dir == 'U':
        cur_pos = (positions_h[ph][0]-1, positions_h[ph][1])
        positions_h.append(cur_pos)
      if dir == 'D':
        cur_pos = (positions_h[ph][0]+1, positions_h[ph][1])
        positions_h.append(cur_pos)
      if dir == 'R':
        cur_pos = (positions_h[ph][0], positions_h[ph][1]+1)
        positions_h.append(cur_pos)
      if dir == 'L':
        cur_pos = (positions_h[ph][0], positions_h[ph][1]-1)
        positions_h.append(cur_pos)
      ph += 1

      #grid = update_grid(grid, positions_h[ph], positions_h[ph-1], 'H')
      if not check_touch(positions_h[ph], positions_t[pt]):
        positions_t.append(positions_h[ph-1])
        #grid = update_grid(grid, positions_h[ph-1], positions_t[pt], 'T')
        #if positions_h[ph] == positions_t[pt]:
        #  grid[positions_h[ph][0]][positions_h[ph][1]] = 'H'
        pt += 1
      else:
        positions_t.append(positions_t[pt])
        pt += 1

      #input()
      # Show grid
      #print_grid(grid)
      #print(f"Positions H: {positions_h}")
      #print(f"Positions T: {positions_t}")
      #sleep(1)
      #input()

print(f"Number positions T: {len(positions_t)}")
print(f"First part - number unique positions T: {len(set(positions_t))}")
# Result: 6339

## Second part

grid = [['.' for _ in range(40)] for _ in range(40)]

positions_h = list()
ph = 0
start_pos = (10, 10)
positions_h = []
positions_h.append(start_pos)
grid[start_pos[0]][start_pos[1]] = 'H'

with open('example-2.txt') as file:
  lines = file.readlines()
  for i in range(len(lines)):
    dir = lines[i].strip()[0:1]
    num = int(lines[i].strip()[1:])
    for i in range(num):
      print_grid(grid)
      print(positions_h)
      sleep(1)
      if dir == 'U':
        cur_pos = (positions_h[ph][0]-1, positions_h[ph][1])
        positions_h.append(cur_pos)
      if dir == 'D':
        cur_pos = (positions_h[ph][0]+1, positions_h[ph][1])
        positions_h.append(cur_pos)
      if dir == 'R':
        cur_pos = (positions_h[ph][0], positions_h[ph][1]+1)
        positions_h.append(cur_pos)
      if dir == 'L':
        cur_pos = (positions_h[ph][0], positions_h[ph][1]-1)
        positions_h.append(cur_pos)
      ph += 1

      grid[positions_h[len(positions_h)-1][0]][positions_h[len(positions_h)-1][1]] = 'H'
      for p in range(len(positions_h)-1):
        if p <= len(positions_h) - 11:
          grid[positions_h[p][0]][positions_h[p][1]] = '.'
        else:
          grid[positions_h[p][0]][positions_h[p][1]] = str(len(positions_h)-p-1)
        #grid = update_grid(grid, positions_h[p], positions_h[p-1], 'H')
