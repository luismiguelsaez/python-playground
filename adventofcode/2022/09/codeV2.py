from time import sleep
from itertools import product

class node:
  def __init__(self, x):
    self.position = x
    self.position_track = list()
    self.position_track.append(x)
  def set_position(self, x):
    self.position = x
    self.position_track.append(x)
  def get_position(self):
    return self.position
  def get_position_track(self):
    return self.position_track
  def get_last_position(self):
    if len(self.position_track) <= 1:
      return self.position
    else:
      return self.position_track[-2]

def print_grid(g: list)->None:
  for l in g:
    print(*l)

def rope_init(input_lines: list, num: int)->list:

  # Define grid
  grid_size = 40
  grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
  print_enabled = True

  # Initialize rope nodes to initial position (0, 0)
  rope = [node((20, 20)) for _ in range(num)]

  #for n in range(len(rope)):
  #  print(f"Node [{n}] position {rope[n].get_position()}")

  if print_enabled:
    grid[20][20] = 's'
    for n in range(len(rope)-1, -1, -1):
      pos = rope[n].get_position()
      if n == 0:
        grid[pos[1]*-1][pos[0]] = 'H'
      else:
        grid[pos[1]*-1][pos[0]] = str(n)
    print_grid(grid)
    input()

  directions = {'R':(1, 0), 'L':(-1, 0), 'U':(0, 1), 'D':(0, -1)}

  for dir, steps in input_lines:
    for _ in range(int(steps)):
      # Set new position for head node
      rope[0].set_position((rope[0].get_position()[0] + directions[dir][0], rope[0].get_position()[1] + directions[dir][1]))

      # Update nodes positions
      for n in range(1,len(rope)):
        parent_position = rope[n-1].get_position()
        node_position = rope[n].get_position()
        if abs(parent_position[0] - node_position[0]) > 1 or abs(parent_position[1] - node_position[1]) > 1:
          middle_position = (int((parent_position[0]+node_position[0])/2), int((parent_position[1]+node_position[1])/2))
          rope[n].set_position(middle_position)

      if print_enabled:
        grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
        grid[20][20] = 's'
        for n in range(len(rope)-1, -1, -1):
          pos = rope[n].get_position()
          if n == 0:
            grid[pos[1]*-1][pos[0]] = 'H'
          else:
            grid[pos[1]*-1][pos[0]] = str(n)
        print_grid(grid)
        input()

  return rope[-1].position_track

def main():
  input = [x for x in map(lambda x: x.split(), [ (x.strip()) for x in open('example-2.txt').readlines() ])]
  print(len(set(rope_init(input, 10))))


main()
