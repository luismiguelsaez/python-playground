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
                      (c_pos[0]+1, c_pos[1]+1),(c_pos[0]-1, c_pos[1]-1),(c_pos[0]-1, c_pos[1]+1),(c_pos[0]+1, c_pos[1]-1) ]:
    return False
  else:
    return True

p = 0
start_pos = (10, 10)
positions_h = []
positions_h.append(start_pos)
positions_t = []
positions_t.append(start_pos)

grid[start_pos[0]][start_pos[1]] = 'T'
grid[start_pos[0]][start_pos[1]] = 'H'

with open('example.txt') as file:
  lines = file.readlines()
  for i in range(len(lines)):
    dir = lines[i].strip()[0:1]
    num = int(lines[i].strip()[1:])
    for i in range(num):
      if dir == 'U':
        cur_pos = (positions_h[p][0]-1, positions_h[p][1])
        positions_h.append(cur_pos)
      if dir == 'D':
        cur_pos = (positions_h[p][0]+1, positions_h[p][1])
        positions_h.append(cur_pos)
      if dir == 'R':
        cur_pos = (positions_h[p][0], positions_h[p][1]+1)
        positions_h.append(cur_pos)
      if dir == 'L':
        cur_pos = (positions_h[p][0], positions_h[p][1]-1)
        positions_h.append(cur_pos)
      p += 1

      # Show grid
      print_grid(grid)
      #grid[positions_t[-1][0]][positions_t[-1][1]] = 'T'
      grid = update_grid(grid, positions_h[p], positions_h[p-1], 'H')
      if not check_touch(positions_h[p], positions_t[-1]):
        print(f"Not in touch {p}")
      sleep(5)

#print(positions_h)
