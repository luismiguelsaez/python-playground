import threading
from time import sleep

def main():

  data = [x.strip() for x in open('input.txt').readlines()]
  signal_strenght = 0
  register = 1
  cycles = [0 for _ in range(len(data)) ]

  for i in range(len(data)):

    if data[i].split()[0] == 'noop':
      pass
    else:
      inc = data[i].split()[1]
      cycles[i+2] += int(inc)

  for j in range(len(cycles)):
    register += cycles[j]
    cycles[j] = register
    strenght = (j+1) * register
    if j+1 == 20 or (j+1 - 20) % 40 == 0:
      print(f"At cycle {j+1} register: {cycles[j]}, strenght: {strenght}")
      signal_strenght += strenght

  print(cycles)
  print(signal_strenght)

main()
