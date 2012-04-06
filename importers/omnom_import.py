#!/usr/bin/env python

import os
import sys
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
from diriwa.models import *
from feedparser import parse
import settings
settings.DEBUG = False
from django.db import transaction

#country = Region.objects.get(shortname=line[0])
f = parse(settings.OMNOM_FEED)
if not f:
    print >>sys.stderr, '[!] cannot parse feed'
    sys.exit(1)

tmap=dict([(''.join(top.name.lower().split()), top)
           for top in Topic.objects.all()])
topics=tmap.keys()
cmap=dict([(''.join(reg.shortname.lower().split()), reg)
           for reg in Region.objects.all()])
countries=cmap.keys()

with transaction.commit_on_success():
   for item in reversed(f['entries']):
      ts=[]
      cs=[]
      for tag in item.get('tags',[]):
         if tag.get('term','').lower() in countries:
            cs.append(tag.get('term'))
         if tag.get('term','').lower() in topics:
            ts.append(tag.get('term'))
      if ts:
         newsitem, created = NewsItem.objects.get_or_create(headline=item.get('title'),
                                                            url=item['links'][0]['href'])
         if created:
            newsitem.text=''.join([x.value for x in item.content])
            newsitem.save()
            # add tags from bookmark
            for tag in item.get('tags',[]):
               if tag in cs or tag in ts: continue
               t=Tag.objects.get_or_create(name=tag['term'])[0]
               EntityTag.objects.get_or_create(entity=newsitem, tag=t)
            # link topics to newsitem
            for t in ts:
               if not t.strip(): continue
               newsitem.itemref.add(tmap[t])
            # link countries to newsitem
            for c in cs:
               if not c.strip(): continue
               newsitem.itemref.add(cmap[c])
