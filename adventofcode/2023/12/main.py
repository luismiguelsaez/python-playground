from sys import argv
import re, itertools, time

lines = [(l.rstrip().split(' ')) for l in open(argv[1], 'r').readlines()]

total_st = time.time()
total_sum = 0
for l in lines:
    line_st = time.time()

    qmarks = [ i.span() for i in re.finditer('\\?', l[0]) ]
    hashes = [ i.span() for i in re.finditer('\\#', l[0]) ]
    total_hashes = sum(list(map(lambda x:int(x), l[1].split(','))))
    regex = '\\.*(#{' + '})\\.+(#{'.join(l[1].split(',')) + '})\\.*'
    
    combinations = list(itertools.combinations_with_replacement(qmarks, total_hashes - len(hashes)))
    combinations_num = 0
    for combination in combinations:
        pattern = list(l[0])
        for char in combination:
            pattern[char[0]] = '#'

        pattern_str = ''.join([ '.' if i == '?' else i for i in pattern ])
        if re.match(regex, pattern_str):
            #print(pattern_str, l[1])
            combinations_num += 1

    line_et = time.time()
    line_elapsed_time = line_et - line_st
    total_sum += combinations_num
    print(f"{l[0]} {l[1]} - tested {len(combinations)} combinations in {line_elapsed_time} secs - found {combinations_num} arrangement(s)")

total_et = time.time()
total_elapsed_time = total_et - total_st
print(f"Total elapsed time: {total_elapsed_time}")

print(f"Part one: {total_sum}")
