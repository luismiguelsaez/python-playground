from random import randrange

def create_panel(size: int, content: str='x')->list:

  panel = [[ content for i in range(size)] for j in range(size)]
  return panel

def place_mines(panel: list, num: int, content: str='o')->list:

  s = len(panel)

  combinations = [(i, j) for i in range(s) for j in range(s)]

  for _ in range(num):
    z = randrange(len(combinations))
    x = combinations[z][0]
    y = combinations[z][1]
    panel[x][y] = content
    del combinations[z]

  return panel

def main():
  test_panel = create_panel(size=4) 
  place_mines(panel=test_panel, num=8)

  for i in test_panel:
    print(*i)

main()
