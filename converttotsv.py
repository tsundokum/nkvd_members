import json
import csv

from itertools import chain
from yargy import Parser, rule, and_, or_
from yargy.predicates import gram, is_capitalized, dictionary, in_, normalized, eq, caseless, type
from yargy.interpretation import fact
from rules import POSITION
# how to extract job description from the crawled data
# table columns order: [marker, preposition, date, position, source, unit]
CRAWLED_DATA = 'members.jl'

pos_parser = Parser(POSITION)

def parse(d):
    for match in pos_parser.findall(d):
        b, e = match.tokens[0].span[0], match.tokens[-1].span[1]
        return  d[b:e],  d[e+1:]
    return '', ''

# for d in data:
#     print('>>>', d)
#
#     p, r = parse(d)
#     print(p)
#     print(r)


data = []
with open(CRAWLED_DATA) as f:
    for line in f:
        j = json.loads(line)
        name = j['name']
        positions = []
        dates = []
        markers = []
        for row in j['table']:
            positions.append(row[3]) #todo: filter out nones
        for date in j['table']:
            dates.append(row[2])
        for marker in j['table']:
            markers.append(row[0])
        data.append([name, markers, dates, positions])


failed_parses = []
with open('positions.tsv','w') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['name', 'marker','date','position','unit'])
    for member in data:
        for i in range(len(member[1])):
            d = member[3][i]
            date = member[2][i]
            marker = member[1][i]
            if d:
                p, r = parse(d)
                if not p:
                    failed_parses.append(d)
            else:
                p = ''
                r = ''
            w.writerow([member[0], marker, date, p, r])

with open('failed_parses.txt','w') as f:
    for line in sorted(failed_parses):
        print(line, file = f)


# examples = ['Особоуполномоченный НКВД СССР', 'авиатехник авиаэскадрильи']
# for ex in examples:
#      p,r = parse(ex)
#      if not p and not r:
#          print(ex)