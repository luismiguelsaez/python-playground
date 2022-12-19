from time import sleep
import curses

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

  # Initialize rope nodes to initial position (0, 0)
  rope = [node((10, 10)) for _ in range(num)]

  for n in range(len(rope)):
    print(f"Node [{n}] position {rope[n].get_position()}")

  for move in input_lines:
    dir, steps = move.split()
    for _ in range(int(steps)):

      head_x, head_y = rope[0].get_position()
      if dir == 'R':
        head_x += 1
        print("Move to the right")
      if dir == 'L':
        head_x -= 1
        print("Move to the left")
      if dir == 'U':
        head_y += 1
        print("Move up")
      if dir == 'D':
        head_y -= 1
        print("Move down")
      
      # Set new position for head node
      rope[0].set_position((head_x, head_y))
      print(f"Node [{0}] position {rope[0].get_position()}")

      # Update nodes positions
      for n in range(1,len(rope)):
        parent_position = rope[n-1].get_position()
        node_position = rope[n].get_position()
        if abs(parent_position[0] - node_position[0]) > 1 or abs(parent_position[1] - node_position[1]) > 1: # to fix
          # Find nearest point to parent
          parent_last_position = rope[n-1].get_last_position()
          rope[n].set_position(parent_last_position)
        print(f"Node [{n}] position {rope[n].get_position()}")

  return rope[-1].position_track

def main():
  input = [ x.strip() for x in open('example-2.txt').readlines() ]
  print(len(set(rope_init(input, 2))))


main()
