from requests import get
from time import sleep

# Get session cookie after login to adventofcode.com
session = '53616c7465645f5f2596cddc32bc251ebdc3b21070bbf3af3f2bd32ac8054d7793c9a0bf8affc014c500bff2c2e337c5dcc62093649140fb38d28f4a8795f288'
res = get('https://adventofcode.com/2022/day/5/input', cookies={'session': session})
input = res.text

def get_moves(lines: list)->list:
  move_lines = filter(lambda x:"".join(x[0:4]) == 'move', lines)
  return list(move_lines)

def print_packets(packets: list)->None:
  for line in packets:
    print('[', end='')
    print(*line, sep='][', end=']\n')

def get_packet(packets: list, col: int):
  packet = ' '
  for line in range(len(packets)):
    cur_packet = packets[line][col-1]
    if cur_packet != ' ':
      packet = cur_packet
      packets[line][col-1] = ' '
      break

  return packet, packets

def put_packet(packets: list, col: int, packet: str)->list:
  # Check if there is an empty position an insert a new file if not
  if packets[0][col-1] != ' ':
    packets.insert(0,[' ' for x in range(len(packets[0])) ])

  # Put packet in destination column
  for line in range(len(packets)):
    cur_packet = packets[line][col-1]
    if cur_packet != ' ':
      packets[line-1][col-1] = packet
      break
    elif line == len(packets)-1:
      packets[line][col-1] = packet
      break

  return packets


packets = [
            ['Q','J',' ',' ',' ',' ',' ',' ','H'],
            ['G','S','Q',' ','Z',' ',' ',' ','P'],
            ['P','F','M',' ','F',' ','F',' ','S'],
            ['R','R','P','F','V',' ','D',' ','L'],
            ['L','W','W','D','W','S','V',' ','G'],
            ['C','H','H','T','D','L','M','B','B'],
            ['T','Q','B','S','L','C','B','J','N'],
            ['F','N','F','V','Q','Z','Z','T','Q']
          ]

lines = get_moves(input.split('\n'))
for i in range(len(lines)):
  data = lines[i].split(' ')
  iterations = int(data[1])
  col_from = int(data[3])
  col_to = int(data[5])

  #print(f"Moving packets from {col_from} to {col_to} {iterations} times")
  for x in range(iterations):
    packet, packets = get_packet(packets, col_from)
    packets = put_packet(packets, col_to, packet)
    #print_packets(packets)
    #print()
    #sleep(1)

print_packets(packets)

# First part
# [ ][ ][ ][ ][ ][ ][ ][ ][ ]
# [ ][ ][ ][ ][ ][ ][ ][M][ ]
# [ ][ ][ ][ ][J][ ][ ][P][ ]
# [ ][ ][ ][ ][F][ ][ ][F][ ]
# [ ][ ][ ][ ][F][ ][ ][Z][ ]
# [ ][G][ ][ ][S][ ][ ][T][N]
# [ ][C][ ][ ][P][ ][ ][T][R]
# [ ][Q][ ][ ][S][ ][R][P][S]
# [ ][M][ ][ ][D][ ][N][Z][Q]
# [ ][Q][ ][ ][V][ ][J][F][T]
# [ ][B][ ][ ][W][ ][Q][L][L]
# [ ][F][ ][ ][W][ ][B][H][Q]
# [V][D][ ][ ][Z][C][H][V][F]
# [L][G][B][B][L][W][H][D][S]
# Answer: VGBBJCRMN

# Reset packets arrangement
packets = [
            ['Q','J',' ',' ',' ',' ',' ',' ','H'],
            ['G','S','Q',' ','Z',' ',' ',' ','P'],
            ['P','F','M',' ','F',' ','F',' ','S'],
            ['R','R','P','F','V',' ','D',' ','L'],
            ['L','W','W','D','W','S','V',' ','G'],
            ['C','H','H','T','D','L','M','B','B'],
            ['T','Q','B','S','L','C','B','J','N'],
            ['F','N','F','V','Q','Z','Z','T','Q']
          ]

def get_packets(packets: list, col: int, num: int):
  packet_batch = []
  for _ in range(num):
    for line in range(len(packets)):
      cur_packet = packets[line][col-1]
      if cur_packet != ' ':
        packet_batch.append(cur_packet)
        packets[line][col-1] = ' '
        break

  return packet_batch, packets

for i in range(len(lines)):
  data = lines[i].split(' ')
  iterations = int(data[1])
  col_from = int(data[3])
  col_to = int(data[5])

  #print(f"Moving {iterations} packets from {col_from} to {col_to}")
  packet_batch,_ = get_packets(packets, col_from, iterations)
  for p in reversed(packet_batch):
    put_packet(packets, col_to, p)
  #print()
  #print_packets(packets)
  #sleep(20)

print_packets(packets)

# Second part
# [ ][ ][ ][ ][ ][ ][ ][M][ ]
# [ ][ ][ ][ ][J][ ][ ][V][ ]
# [ ][ ][ ][ ][H][ ][ ][P][ ]
# [ ][ ][ ][ ][S][ ][ ][F][ ]
# [ ][B][ ][ ][R][ ][ ][J][H]
# [ ][S][ ][ ][F][ ][ ][M][S]
# [ ][T][ ][ ][Q][ ][R][C][Z]
# [ ][C][ ][ ][B][ ][P][T][H]
# [ ][W][ ][ ][Q][ ][D][W][L]
# [ ][L][ ][ ][Z][ ][L][W][Q]
# [ ][V][ ][ ][Z][ ][N][F][P]
# [L][Q][ ][ ][T][B][D][F][D]
# [S][N][B][V][Q][G][F][G][F]
# Answer: LBBVJBRMH
