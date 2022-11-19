from itertools import permutations
from timeit import timeit

def twoArrays(k, A, B):
    
    pA = list(permutations(A))
    pB = list(permutations(B))

    for i in range(len(pA)):
        for j in range(len(pB)):
            print("Calculating:", pA[i], pB[j])
            s = [x + y for x,y in zip(pA[i], pB[j]) if x + y >= k ]
            
            if len(s) == len(pA[i]):
                print("- i:",pA[i])
                print("- j:",pB[j])
                print("- s:",s)
                return 'YES'

    return 'NO'

def twoArraysAlt(k, A, B):
    
    c = 0
    for i in permutations(A):
        for j in permutations(B):
            c += 1
            print(f"[{c}] Calculating: {i} {j}")
            s = [x + y for x,y in zip(i, j) if x + y >= k ]
            
            if len(s) == len(i):
                print("- i:",i)
                print("- j:",j)
                print("- s:",s)
                return 'YES'

    return 'NO'

def main():
  # NO
  a = [18, 73, 55, 59, 37, 13, 1, 33]
  b = [81, 11, 77, 49, 65, 26, 29, 49]
  #print("RES", twoArraysAlt(91, a, b))

  # YES
  a = [ 84, 2, 50, 51, 19, 58, 12, 90, 81, 68, 54, 73, 81, 31, 79, 85, 39, 2 ]
  b = [ 53, 102, 40, 17, 33, 92, 18, 79, 66, 23, 84, 25, 38, 43, 27, 55, 8, 19 ]
  #print("RES", twoArraysAlt(94, a, b))

  # YES
  a = [ 15, 16, 44, 58, 5, 10, 16, 9, 4, 20, 24 ]
  b = [ 37, 45, 41, 46, 8, 23, 59, 57, 51, 44, 59 ]
  #print("RES", twoArraysAlt(59, a, b))

  # YES
  a = [ 4, 4, 3, 2, 1, 4, 4, 3, 2, 4 ]
  b = [ 2, 3, 0, 1, 1, 3, 1, 0, 0, 2 ]
  #print("RES", twoArraysAlt(4, a, b))
  print(twoArraysAlt(4, a, b))

  # YES
  a = [ 3, 6, 8, 5, 9, 9, 4, 8, 4, 7 ]
  b = [ 5, 1, 0, 1, 6, 4, 1, 7, 4, 3 ]
  #print("RES", twoArraysAlt(9, a, b))

main()
