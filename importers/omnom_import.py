#!/usr/bin/env python

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

topics=[''.join(top.name.lower().split())
        for top in Topic.objects.all()]
countries=[''.join(reg.shortname.lower().split())
           for reg in Region.objects.filter(type=RegionType.objects.get(name="Country"))]

for item in reversed(f['entries']):
   ts=[]
   cs=[]
   for tag in item.get('tags',[]):
      if tag.get('term','').lower() in countries:
         cs.append(tag.get('term'))
      if tag.get('term','').lower() in topics:
         ts.append(tag.get('term'))
   if ts and cs:
      print item['links'][0]['href']
      print item.get('title')
      print '\t', ', '.join(cs)
      print '\t', ', '.join(ts)
      print ''.join([x.value for x in item.content])
      #NewsItem.objects.get_or_create()
      #headline		= models.CharField(max_length=200)
      #text			= models.TextField()
      #itemref			= models.ForeignKey(Entity, blank=True, null=True)
      #author			= models.ForeignKey(User, blank=True, null=True)
      #timestamp_submitted	= models.DateTimeField(auto_now_add=True)
      #timestamp_edited	= models.DateTimeField(auto_now=True)
