import re
import concurrent.futures
import time
from sys import argv
import cProfile

lines = [ l.rstrip() for l in open(argv[1], 'r').readlines() ]

map_scan = False
map_lines = []
map_header = ""
almanaq = {}
for line in lines:

    #almanaq['seeds'] = re.findall('^seeds:\\s(.*)$', line)[0].split(' ')
    seeds_header_match = re.search('^[a-z-]+:\\s(.*)$', line)
    if seeds_header_match is not None:
        seeds = seeds_header_match.groups()[0]
        seeds_list = list(map(lambda x: int(x), seeds.split(' ')))
        almanaq['seeds'] = seeds_list
        #print(f"Seeds: {seeds}")

    #map_header = re.findall('^([a-z-]+)\\smap:.*$', line)
    #if len(map_header) != 0:
    #    almanaq[map_header] = []

    maps_header_match = re.search('^([a-z-]+)\\smap:$', line)
    if maps_header_match is not None:
        map_header = maps_header_match.groups()[0]
        almanaq[map_header] = []
        #print(f"Map header: {map_header}")
        map_scan = True
        map_lines = []
        continue

    if map_scan:
        if line == '':
            map_scan = False
            almanaq[map_header] = sorted(map_lines, key=lambda x: x[2])
            #print(f" - {map_lines}")
            continue
        else:
            map_lines.append(list(map(lambda x: int(x), line.split(' '))))

almanaq[map_header] = map_lines
#print(f" - {map_lines}")

def get_mapping_value(mapping_lines: list, src_value: int)->int:
    dst_value = 0
    mapping_lines_len = len(mapping_lines)
    for line in range(mapping_lines_len):
        dst_range_start, src_range_start, range_length = mapping_lines[line]
        src_range = range(src_range_start, src_range_start + range_length)
        dst_range = range(dst_range_start, dst_range_start + range_length)

        if src_value in src_range:
            src_idx = src_range.index(int(src_value))
            dst_value = dst_range[ src_idx ]
            break
        else:
            dst_value = src_value

    return dst_value

seeds = almanaq['seeds']
locations = []
for seed in seeds:
    #print(f"- Seed: {seed}")

    soil = get_mapping_value(almanaq['seed-to-soil'], seed)
    fertilizer = get_mapping_value(almanaq['soil-to-fertilizer'], soil)
    water = get_mapping_value(almanaq['fertilizer-to-water'], fertilizer)
    light = get_mapping_value(almanaq['water-to-light'], water)
    temperature = get_mapping_value(almanaq['light-to-temperature'], light)
    humidity = get_mapping_value(almanaq['temperature-to-humidity'], temperature)
    location = get_mapping_value(almanaq['humidity-to-location'], humidity)

    locations.append(location)

    #print(f"   --> Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}")

print(f"Part one: {min(locations)}")

ranges = [range(int(almanaq['seeds'][i]), int(almanaq['seeds'][i]) + int(almanaq['seeds'][i+1])) for i in range(len(almanaq['seeds'])) if i == 0 or i % 2 == 0 ]
sorted_ranges = sorted(ranges, key=lambda x: x.start)

def solve_range(r):
    location_min = -1
    range_len = len(r)
    for seed in range(range_len):
        #st = time.process_time()
        #print(f"- Solving seed for range [{r}] {seed}/{range_len}")
        soil = get_mapping_value(almanaq['seed-to-soil'], r[seed])
        fertilizer = get_mapping_value(almanaq['soil-to-fertilizer'], soil)
        water = get_mapping_value(almanaq['fertilizer-to-water'], fertilizer)
        light = get_mapping_value(almanaq['water-to-light'], water)
        temperature = get_mapping_value(almanaq['light-to-temperature'], light)
        humidity = get_mapping_value(almanaq['temperature-to-humidity'], temperature)
        location = get_mapping_value(almanaq['humidity-to-location'], humidity)
        #et = time.process_time()
        #print(f"- CPU execution time for range [{r}] and seed[{seed}]: {et - st } seconds")
        if ( range_len - seed ) % 100000 == 0:
            print(f"Solved range [{r}] {seed}/{range_len}: {seed / range_len * 100}%")

        if location_min == -1 or location < location_min:
            location_min = location

    return location_min

results = []

#for r in range(len(sorted_ranges)):
#    st = time.process_time()
#    print(f"-- Solving range [{sorted_ranges[r]}]")
#    results.append(solve_range(sorted_ranges[r]))
#    et = time.process_time()
#    print(f"-- CPU execution time for range [{sorted_ranges[r]}]: {et - st } seconds")

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = {executor.submit(solve_range, r): r for r in sorted_ranges}
    for future in concurrent.futures.as_completed(futures):
        res = futures[future]
        results.append(future.result())

print(f"Part two: {min(results)}")
