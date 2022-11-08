from random import randrange

def flip_row(matrix: list[list], row: int)->list[list]:

  matrix[row] = matrix[row][::-1]

  return matrix


def flip_col(matrix: list[list], col: int)->list[list]:

  column = []
  for i in range(len(matrix)):
    column.append(matrix[i][col])
  
  column = column[::-1]
  for i in range(len(matrix)):
    matrix[i][col] = column[i]

  return matrix


def sum_quadrant(matrix: list[list])->int:

  sum = 0
  for i in range(len(matrix)//2):
    for j in range(len(matrix[i])//2):
      sum += matrix[i][j]

  return sum


def main():

  size = 4
  test_matrix = [ [randrange(10) for j in range(size)] for i in range(size)]

  print("- Initial matrix")
  for r in range(len(test_matrix)):
    print(*test_matrix[r])

  max = 0
  for i in range(len(test_matrix)):
    tmp_matrix = test_matrix[:]
    for j in range(len(test_matrix)):
      tmp_matrix = flip_row(tmp_matrix, i)
      tmp_matrix = flip_col(tmp_matrix, j)
      tmp_sum = sum_quadrant(tmp_matrix)
      if tmp_sum > max:
        max = tmp_sum

      print()
      print("- Flipped row:",i,"col:",j)
      for r in range(len(tmp_matrix)):
        print(*tmp_matrix[r])
      print("- Sum:", tmp_sum)

      print()
  
  print("- Max sum:", max)

main()
