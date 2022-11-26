from itertools import permutations
from time import time_ns
from random import randrange


def maxMin_(k, arr):
    res = list()
    for i in list(permutations(arr,k)):
        res.append((max(i) - min(i)))

    return min(res)

# Optimized function
def maxMin(k, arr):
  sarr = sorted(arr, reverse=True)
  mins = 0
  for i in range(0, len(sarr)-k+1):
    sub = sarr[i:k+i]
    d = sub[0] - sub[-1]
    if i == 0:
      mins = d
    else:
      if d < mins:
        mins = d
  
  return mins


arr = [randrange(99999999) for i in range(100000)]

i = time_ns()
print(maxMin(60000, arr))
print("Time:",time_ns()-i)