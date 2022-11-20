from random import randrange

get_matrix = lambda size, content: [[content for y in range(size)] for i in range(size)]

def fill_random(l: list, num: int)->list[list]:
  max = len(l)

  for _ in range(num):
    l[randrange(max)][randrange(max)] = randrange(10)

  return l

def main():
  test_matrix = get_matrix(10, 0)
  test_matrix = fill_random(test_matrix, 50)

  for i in test_matrix:
    print(*i)


if __name__ == "__main__":
  main()