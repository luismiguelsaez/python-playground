from random import randrange

def create_panel(size: int, content: str='x')->list:

  panel = [[ content for i in range(size)] for j in range(size)]
  return panel

def place_mines(panel: list, num: int, content: str='o')->list:

  s = len(panel)

  combinations = [(i, j) for i in range(s) for j in range(s)]
  mines = []

  for _ in range(num):
    z = randrange(len(combinations))
    x = combinations[z][0]
    y = combinations[z][1]
    panel[x][y] = content
    del combinations[z]
    mines.append((x, y))

  return panel

def place_numbers(panel: list, content: str='o')->list:

  corners = [(0, 0), (len(panel)-1, len(panel)-1), (0, len(panel)-1), (len(panel)-1, 0)]

  for i in range(len(panel)):
    for j in range(len(panel)):
      if panel[i][j] != content:
        if (i, j) in corners:
          print(f"Corner {i} {j} not a mine")
        elif i == 0 or j == 0 or i == len(panel)-1 or j == len(panel)-1:
          print(f"Lateral {i} {j} not a mine")
        else:
          print(f"{i} {j} not a mine")

  return []

def main():
  test_panel = create_panel(size=6) 
  place_mines(panel=test_panel, num=6)

  for i in test_panel:
    print(*i)

  print()
  place_numbers(test_panel)

main()
