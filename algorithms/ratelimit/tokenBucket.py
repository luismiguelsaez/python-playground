
input_data = [1,1,1,1,1,2,2,2,4,4,4,4,4,6,6,6,8,8,8,8,8,9,9,9,9,9,9,10,10,10,11,11,11,11,12,12,12,13,13]

buckets = {
  1: { "max": 4,  "cur": 4,  "t_ini": 0 },
  5: { "max": 10, "cur": 10, "t_ini": 0 }
}

for i in range(len(input_data)):
  
  for b in buckets:
    if i == 0: buckets[b]['t_ini'] = input_data[i]

    if input_data[i] - buckets[b]['t_ini'] >= b:
      buckets[b]['cur'] = buckets[b]['max']
      buckets[b]['t_ini'] = input_data[i]
    
    buckets[b]['cur'] -= 1

    if buckets[b]['cur'] < 0:
      res = 'drop'
      break
    else:
      res = 'forward'

  print(input_data[i], buckets[5]['cur'], res)
