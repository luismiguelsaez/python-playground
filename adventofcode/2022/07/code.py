
with open('example.txt') as file:
  lines = file.readlines()

cur_dir = ''
sum_sw = False
sum_dir = {}

route = []

for i in range(len(lines)):
  line = lines[i].strip()
  if line[0] == '$':
    cmd = line[2:]
    if cmd[0:2] == 'cd':
      if cmd[3:5] == '..':
        route.pop()
      else:
        cur_dir = cmd[3:]
        route.append(cur_dir)
      print(f"Current path: {route} - /{'/'.join(route[1:])}")
      #print(f"Change to dir {cur_dir}")
    elif cmd[0:2] == 'ls':
      pass
  else:
    if line[0:3] == 'dir':
      dir_name = line[4:]
      #print(f"Adding dir {dir_name} to cur dir {cur_dir}")
      #if cur_dir in sum_dir:
      #  sum_dir[cur_dir] += int(sum_dir[dir_name])
      #else:
      #  sum_dir[cur_dir] = int(sum_dir[dir_name])
      #print(f"  Dir {line[4:]} in dir {cur_dir}")
      pass
    else:
      f_size = line.split(' ')[0]
      f_name = line.split(' ')[1]
      #print(f"  File {f_name} in dir {cur_dir}")
      #print(f"Adding file {f_name}/{f_size} to dir {cur_dir}")
      if cur_dir in sum_dir:
        sum_dir[cur_dir] += int(f_size)
      else:
        sum_dir[cur_dir] = int(f_size)


exit()
sum_total = 0
for dir in list(filter(lambda x: x[1] > 100000,sorted(sum_dir.items(), key=lambda x:x[1]))):
  sum_total += dir[1]

print(f"Dirs: {sum_dir}")
print("Total:", sum_total)
