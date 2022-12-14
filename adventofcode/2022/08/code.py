
with open('input.txt') as file:
  matrix = [[i for i in j.strip()] for j in file.readlines()]

def print_wood(matrix: list)->None:
  for line in matrix:
    print(*line)

def get_inner_visible_trees(matrix: list)->int:
  visible_trees = 0
  for x in range(len(matrix))[1:-1]:
    for y in range(len(matrix[x]))[1:-1]:
      height = matrix[x][y]
      right = [i for i in matrix[x][y+1:] if i >= height]
      left = [i for i in matrix[x][:y] if i >= height]
      up = [i for i in [matrix[a][y] for a in range(len(matrix))[0:x]] if i >= height]
      down = [i for i in [matrix[a][y] for a in range(len(matrix))[x+1:]] if i >= height]
      if not ( right and left and up and down ):
        visible_trees += 1
  return visible_trees

def check_visibility(h: int, trees: list)->int:
  count = 0
  for i in range(len(trees)):
    count += 1
    if trees[i] >= h:
      break
  return count

def get_number_visible_trees(matrix: list)->int:
  max_visible_trees = 0
  for x in range(len(matrix))[1:-1]:
    for y in range(len(matrix[x]))[1:-1]:
      height = matrix[x][y]
      right_trees = matrix[x][y+1:]
      right = check_visibility(height, right_trees)
      left_trees = list(reversed(matrix[x][:y]))
      left = check_visibility(height, left_trees)
      up_trees = list(reversed([matrix[a][y] for a in range(len(matrix))[0:x]]))
      up = check_visibility(height, up_trees)
      down_trees = [matrix[a][y] for a in range(len(matrix))[x+1:]]
      down = check_visibility(height, down_trees)
      total = up*left*right*down
      if total > max_visible_trees:
        max_visible_trees = total

  return max_visible_trees

def get_outer_trees(matrix: list)->int:
  return len(matrix)*4-4

print(f"First part: {get_inner_visible_trees(matrix) + get_outer_trees(matrix)}")
# Result: 1789

print(f"Second part: {get_number_visible_trees(matrix)}")
# Result: 314820
