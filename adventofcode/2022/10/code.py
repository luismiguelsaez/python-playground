from time import sleep

def main():

  data = [x.strip() for x in open('example.txt').readlines()]
  signal_strength_total = 0
  register = 1
  cycle = 0
  cycle_time = 0.01

  for i in range(len(data)):

    if data[i].split()[0] == 'noop':
      for _ in range(1):
        sleep(cycle_time)
        cycle += 1
        if cycle == 20 or ((cycle - 20) % 40) == 0:
          signal_strength = cycle*register
          signal_strength_total += signal_strength
          print(f"[{cycle}] reg: {register} signal strength: {signal_strength}")
    else:
      inc = int(data[i].split()[1])
      for _ in range(2):
        sleep(cycle_time)
        cycle += 1
        if cycle == 20 or ((cycle - 20) % 40) == 0:
          signal_strength = cycle*register
          signal_strength_total += signal_strength
          print(f"[{cycle}] reg: {register} signal strength: {signal_strength}")
      register += inc

  print(f"Signal strength total: {signal_strength_total}")

main()
