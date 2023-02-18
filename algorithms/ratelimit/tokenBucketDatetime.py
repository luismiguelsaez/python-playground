from datetime import datetime

buckets = {
  1: { 'max': 4,  'cur': 4,  't_ini': '' },
  5: { 'max': 10, 'cur': 10, 't_ini': '' }
}

input_data = [
  '12:30:59', '12:30:59', '12:30:59', '12:30:59', '12:30:59', '12:30:59',
  '13:00:00', '13:00:01', '13:00:01', '13:00:01', '13:00:01', '13:00:01',
  '13:00:03', '13:00:03', '13:00:03', '13:00:04', '13:00:04', '13:00:04',
]

for i in range(len(input_data)):
  if i == 0: buckets[1]['t_ini'] = input_data[i]

  diff = int(datetime.strptime(input_data[i],'%H:%M:%S').strftime("%s")) - int(datetime.strptime(buckets[1]['t_ini'],'%H:%M:%S').strftime("%s"))
  if diff >= 1:
    buckets[1]['cur'] = buckets[1]['max']
    buckets[1]['t_ini'] = input_data[i]
  
  buckets[1]['cur'] -= 1

  if buckets[1]['cur'] < 0:
    res = f'drop bucket {1} execeeded'
    #break
  else:
    res = 'forward'

  print(f"{input_data[i],buckets[1]['cur'], res}")