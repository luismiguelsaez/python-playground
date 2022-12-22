from time import sleep

def main():

  data = [x.strip() for x in open('input.txt').readlines()]
  signal_strength_total = 0
  register = 1
  cycle = 0
  cycle_time = 0
  pixel_pos = 0
  rows = [['.' for _ in range(40)] for _ in range(6)]
  row = 0
  inc = 0

  for i in range(len(data)):
    op = data[i].split()[0]
    cycle_count = 1 if op == 'noop' else 2
    if op == 'addx': inc = int(data[i].split()[1])
    for _ in range(cycle_count):
      sleep(cycle_time) # Only for debugging purposes
      cycle += 1
      pixel_pos = cycle-1 # Pixel position is 0-40, where cycle starts at 1
      row = pixel_pos//40 # Find row number 1-6
      pixel_pos_row = pixel_pos - (row*40) # Calculate pixel position within current row
      if pixel_pos_row in [i for i in range(register-1, register+2)]: # Check if the pixel position falls into sprite positions (3 pixel wide)
        rows[row][pixel_pos_row] = '#'
      if cycle == 20 or ((cycle - 20) % 40) == 0: # Check if we are in the cycle whose signal strength we need to take into account
        signal_strength = cycle*register
        signal_strength_total += signal_strength
    if op == 'addx':register += inc
      
  print(f"Part 1: signal strength total: {signal_strength_total}")
  # Result part 1: 16020
  print(f"Part 2:")
  for r in rows:
    print(*r, sep='')
  # Result part 2:
  ####..##..####.#..#.####..##..#....###..
  #....#..#....#.#..#....#.#..#.#....#..#.
  ###..#......#..#..#...#..#..#.#....#..#.
  #....#.....#...#..#..#...####.#....###..
  #....#..#.#....#..#.#....#..#.#....#.#..
  ####..##..####..##..####.#..#.####.#..#.

main()
