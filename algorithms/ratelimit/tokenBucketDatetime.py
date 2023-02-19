from datetime import datetime

buckets = {
  1: { 'max': 4,  'cur': 4,  't_ini': '' },
  5: { 'max': 10, 'cur': 10, 't_ini': '' }
}

input_data = [
  '12:30:59', '12:30:59', '12:30:59', '12:30:59', '12:30:59', '12:30:59',
  '13:00:00', '13:00:01', '13:00:01', '13:00:01', '13:00:01', '13:00:01',
  '13:00:03', '13:00:03', '13:00:03', '13:00:03', '13:00:03', '13:00:03',
  '13:00:03', '13:00:03', '13:00:03', '13:00:03', '13:00:03', '13:00:03',
  '13:00:04', '13:00:04', '13:00:04', '13:00:04', '13:00:04', '13:00:04',
  '13:00:05', '13:00:06', '13:00:07', '13:00:08', '13:00:09', '13:00:10',
]

b = 1
for i in range(len(input_data)):
  if i == 0: buckets[b]['t_ini'] = input_data[i]

  diff = int(datetime.strptime(input_data[i],'%H:%M:%S').strftime("%s")) - int(datetime.strptime(buckets[b]['t_ini'],'%H:%M:%S').strftime("%s"))
  if diff >= b:
    buckets[b]['cur'] = buckets[b]['max']
    buckets[b]['t_ini'] = input_data[i]
  
  buckets[b]['cur'] -= 1

  if buckets[b]['cur'] < 0:
    res = f'drop bucket {b} execeeded'
    #break
  else:
    res = 'forward'

  print(f"{input_data[i],buckets[b]['cur'], res}")