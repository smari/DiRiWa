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
           for reg in Region.objects.all()]

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
         tag=Tag.objects.get_or_create(name=tag['term'])[0]
         EntityTag.objects.get_or_create(entity=newsitem, tag=tag)
         # link topics to newsitem
         for t in ts:
            top=Topic.objects.get(name__iexact=t)
            newsitem.itemref.add(top)
            print top
         # link countries to newsitem
         for c in cs:
            ctry=Region.objects.get(shortname__iexact=c)
            newsitem.itemref.add(ctry)
            print ctry
