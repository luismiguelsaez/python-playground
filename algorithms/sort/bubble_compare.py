from random import randrange
from copy import deepcopy
import time

def bubble_moving_end(l: list)->list:
  for i in range(len(l)):
      for j in range(0, len(l)-i-1):
          if l[j] > l[j+1]:
              l[j], l[j+1] = l[j+1], l[j]
  
  return l


def bubble(l: list)->list:
  for i in range(len(l)):
    for j in range(len(l)-1):
      if l[j] > l[j+1]:
        l[j], l[j+1] = l[j+1], l[j]
  
  return l


def bubble_sw(l: list)->list:
  sw = True
  c = 0

  while sw:
    c += 1
    sw = False
    for i in range(len(l)-1):
      if l[i] > l[i+1]:
        sw = True
        l[i], l[i+1] = l[i+1], l[i]
  else:      
    print("Exiting loop at iteration:", c)

  return l


def main():
  size = 10000
  rl = [randrange(size) for x in range(size)]

  s = time.time()
  l1 = bubble(deepcopy(rl))
  e = time.time()
  print("Elapsed bubble:", e - s)

  s = time.time()
  l2 = bubble_sw(deepcopy(rl))
  e = time.time()
  print("Elapsed bubble_sw:", e - s)

  s = time.time()
  l3 = bubble_moving_end(deepcopy(rl))
  e = time.time()
  print("Elapsed bubble_moving_end:", e - s)

  for i in range(len(rl)):
    if l1[i] == l2[i] and l2[i] == l3[i]:
      pass
    else:
      print("Error at idx:", i)
      break

main()
