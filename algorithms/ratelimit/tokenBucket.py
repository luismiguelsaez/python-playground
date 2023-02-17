
input_data = [1,1,1,1,1,2,2,2,3,3,3,4,4,4,4,6,6,6,7,7,7,7,8,8,9,9,9,9,9,9,10,10,10,11,11,11,11,12,12,12,13,13]

buckets = {
  1: { "max": 4, "curr": 4, "val": 0 },
  5: { "max": 10, "curr": 4, "val": 0 }
}


for i in range(len(input_data)):

  for bucket,val in buckets.items():
    if input_data[i] % bucket == 0 and buckets[bucket]['val'] != input_data[i]:
      buckets[bucket]['val'] = input_data[i]
      buckets[bucket]['curr'] = buckets[bucket]['max']
    buckets[bucket]['curr'] -= 1

  buckets_status = [x for x,y in buckets.items() if y['curr'] < 0]
  res = "reject" if len(buckets_status) > 0 else "pass"

  print(input_data[i], buckets[1]['val'], buckets[1]['curr'], res)
