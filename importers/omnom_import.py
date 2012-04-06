#!/usr/bin/python

import os
import sys
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from diriwa.models import *
from django.db import transaction
from feedparser import parse
import settings
settings.DEBUG = False

#country = Region.objects.get(shortname=line[0])
f = parse(settings.OMNOM_FEED)
if not f:
    print >>sys.stderr, '[!] cannot parse feed'
    sys.exit(1)

for item in reversed(f['entries']):
   print item['links'][0]['href']
   print item.get('title')
   for tag in item.get('tags',[]):
      if tag.get('term'): print '\t', tag['term'], tag.get('scheme')
