#!/usr/bin/python
#
#
#####

import os
import sys
sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "settings"
import csv 
from diriwa.models import *
from django.db import transaction

if len(sys.argv) < 3:
	print "Usage: regionbuilder.py <countrylist.csv> <type> <region name>"
	print "   Type is: 'Geographic region', 'Union', 'Treaty', 'Block', 'Country'"
	sys.exit(0)

csvfile = open(sys.argv[1], "r")
try:
	dialect = csv.Sniffer().sniff(csvfile.read(1024))
	csvfile.seek(0)
	reader = csv.reader(csvfile, dialect=dialect)
	headers = reader.next()
except:
	csvfile.seek(0)
	print "Not a CSV... falling back to plain text list."
	reader = [[x.strip()] for x in csvfile.readlines()]
	print reader

# Format:
#	[Country, Relationship Type]
#

georegion, created = RegionType.objects.get_or_create(name="Geographic region", in_menu=True)
union, created = RegionType.objects.get_or_create(name="Union")
treaty, created = RegionType.objects.get_or_create(name="Treaty")
bloc, created = RegionType.objects.get_or_create(name="Block")
country, created = RegionType.objects.get_or_create(name="Country")

type = RegionType.objects.get(name__icontains=sys.argv[2])

region, created = Region.objects.get_or_create(name=sys.argv[3], type=type)

if created:
	print "Created new region %s" % region.name
else:
	print "Using existing region %s" % region.name

with transaction.commit_on_success():
   for line in reader:
      try:
         c = Region.objects.get(shortname=line[0])
      except Exception, e:
         try:
            c = Region.objects.get(name=line[0])
         except Exception, e:
            try:
               c = Region.objects.get(shortname__icontains=line[0])
            except Exception, e:
               print e
               print "Couldn't find country name '%s' - check the spelling!" % line[0]
               continue

      if len(line) > 1:
         relationshiptype = line[1]
      else:
         relationshiptype = None

      RegionMembership.objects.get_or_create(region=region, member=c, type=relationshiptype)
      print "Added %s to region %s" % (c.shortname, region.name)
