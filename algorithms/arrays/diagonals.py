import random

def random_matrix(max: int, dim: int) -> list:
  return [[random.randrange(max) for j in range(dim)] for i in range(dim)]

def diag_ul_br(matrix: list) -> list:
  res = []
  for i in range(len(matrix)):
    res.append(matrix[i][i])
  return res

def diag_ur_bl(matrix: list) -> list:
  res = []
  for i in range(len(matrix)):
    res.append(matrix[i][len(matrix)-i-1])
  return res

if __name__ == "__main__":

  matrix = random_matrix(10,5)

  print("\n- RANDOM MATRIX-")
  print(*matrix,sep="\n")

  print("\n- DIAGONALS -")
  print("UpperLeft - BottomRight:",diag_ul_br(matrix))
  print("BottomRight - UpperLeft:",list(reversed(diag_ul_br(matrix))))
  print("UpperRight - BottomLeft:",diag_ur_bl(matrix))
  print("BottomLeft - UpperRight:",list(reversed(diag_ur_bl(matrix))))
