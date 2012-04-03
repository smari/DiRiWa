#!/usr/bin/env python

# -*- coding: utf-8 -*-
#    This file is part of diriwa.
# Usage:
#	python mw-importer.py ../data/legacy/* > ../data/legacy-pages.csv

import sys, re, csv

sectionre=re.compile(r'== (.*) ==')

results=[]
for entity in sys.argv:
    inp=open(entity,'r')
    section=None
    for line in inp.readlines():
        m=sectionre.match(line)
        if m:
            if section and ''.join(section[2]).strip(): results.append(section)
            section=(entity,m.group(1),[])
            #print >>sys.stderr, "new section", section
        elif section:
            section[2].append(line)
    inp.close()
#print results

writer = csv.writer(sys.stdout, dialect="excel")
#writer.writerow(['entity', 'section','text'])
writer.writerows([(v[0], v[1], ''.join(v[2])) for v in results])
