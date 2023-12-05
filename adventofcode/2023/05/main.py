import re

lines = [ l.rstrip() for l in open('input.txt', 'r').readlines() ]

map_scan = False
map_lines = []
map_header = ""
almanaq = {}
for line in lines:

    seeds_header_match = re.search('^[a-z-]+:\\s(.*)$', line)
    if seeds_header_match is not None:
        seeds = seeds_header_match.groups()[0]
        seeds_list = seeds.split(' ')
        almanaq['seeds'] = seeds_list
        #print(f"Seeds: {seeds}")

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
            almanaq[map_header] = map_lines
            #print(f" - {map_lines}")
            continue
        else:
            map_lines.append(line.split(' '))

almanaq[map_header] = map_lines
#print(f" - {map_lines}")

def get_mapping_value(mapping_lines: list, src_value: int)->int:
    dst_value = 0
    for line in mapping_lines:
        dst_range_start, src_range_start, range_length = line
        src_range = range(int(src_range_start), int(src_range_start) + int(range_length))
        dst_range = range(int(dst_range_start), int(dst_range_start) + int(range_length))
        #print(f"  - Source range: {src_range} - Destination range: {dst_range}")

        if int(src_value) in src_range:
            src_idx = src_range.index(int(src_value))
            dst_value = dst_range[ src_idx ]
        if dst_value == 0:
            dst_value = int(src_value)

    return dst_value

seeds = almanaq['seeds']
locations = []
for seed in seeds:
    #print(f"- Seed: {seed}")

    soil = get_mapping_value(almanaq['seed-to-soil'], int(seed))
    fertilizer = get_mapping_value(almanaq['soil-to-fertilizer'], soil)
    water = get_mapping_value(almanaq['fertilizer-to-water'], fertilizer)
    light = get_mapping_value(almanaq['water-to-light'], water)
    temperature = get_mapping_value(almanaq['light-to-temperature'], light)
    humidity = get_mapping_value(almanaq['temperature-to-humidity'], temperature)
    location = get_mapping_value(almanaq['humidity-to-location'], humidity)

    locations.append(location)

    print(f"   --> Seed {seed}, soil {soil}, fertilizer {fertilizer}, water {water}, light {light}, temperature {temperature}, humidity {humidity}, location {location}")

print(f"Part one: {min(locations)}")
