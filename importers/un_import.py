#!/usr/bin/env python
#
#
#####

# -*- coding: utf-8 -*-

import os
import sys
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
import csv 
from diriwa.models import *
import settings
settings.DEBUG = False
from django.db import transaction

csvfile = open("../data/un_treaties.csv")
dialect = csv.Sniffer().sniff(csvfile.read(32768))
csvfile.seek(0)
reader = csv.reader(csvfile, dialect=dialect)
headers = reader.next()

# Chapter,Country,Ratification,Treaty,Signature
# Charter of the United Nations and Statute of the International Court of Justice,Argentina,24 Sep 1945,"Charter of the United Nations (deposited in the archives of the Government of the United States of America). San Francisco, 26 June 1945",

treatytype, created = RegionType.objects.get_or_create(name="Treaty")

with transaction.commit_on_success():
   for line in reader:
      line[3]=line[3].decode('utf8')
      treaty, created = Region.objects.get_or_create(name=line[3], type=treatytype)

      if created:
         print (u"Created treaty %s" % treaty.name).encode('utf8')

      if not line[1].strip(): continue
      line[1]=line[1].decode('utf8')
      try:	signatory = Region.objects.get(name=line[1])
      except:
         try:	signatory = Region.objects.get(shortname=line[1])
         except:
            print (u"Failed to recognize signatory '%s'" % line[1]).encode('utf8')
            continue

      # print signatory
      if line[3]:
         memrel, created = RegionMembership.objects.get_or_create(region=treaty, member=signatory)
         memrel.type = line[3]
         memrel.save()
         if created:
            print (u"Added %s to treaty %s" % (signatory, treaty.name)).encode('utf8')
