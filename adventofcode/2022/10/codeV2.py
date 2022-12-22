from time import sleep

def main():

  data = [x.strip() for x in open('input.txt').readlines()]
  signal_strength_total = 0
  register = 1
  cycle = 0
  cycle_time = 0.01
  pixel_pos = 0
  rows = [[] for _ in range(6)]
  row = 0
  inc = 0

  for i in range(len(data)):
    op = data[i].split()[0]
    cycle_count = 1 if op == 'noop' else 2
    if op == 'addx': inc = int(data[i].split()[1])
    for _ in range(cycle_count):
      sleep(cycle_time)
      cycle += 1
      pixel_pos = cycle-1
      row = pixel_pos//40
      pixel_in_row = pixel_pos - (row*40)
      rows[row] = ['.' for _ in range(40)]
      for i in range(len(rows[row])):
        if i == pixel_in_row:
          rows[row][i] = '#'
      #print(*rows[row])
      #print(f"[{cycle}] Pixel position {pixel_pos} row: {row}")
      if cycle == 20 or ((cycle - 20) % 40) == 0:
        signal_strength = cycle*register
        signal_strength_total += signal_strength
        #print(f"[{cycle}] reg: {register} signal strength: {signal_strength}")
    if op == 'addx':register += inc
      

  print(f"Part 1: signal strength total: {signal_strength_total}")
  # Result part 1: 16020

main()
