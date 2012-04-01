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
#	[Country]
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

for line in reader:
	try:
		c = Country.objects.get(shortname=line[0])
	except Exception, e:
		try:
			c = Country.objects.get(name=line[0])
		except Exception, e:
			try:
				c = Country.objects.get(shortname__icontains=line[0])
			except Exception, e:
				print e
				print "Couldn't find country name '%s' - check the spelling!" % line[0]
				continue

	c.regions.add(region)
	print "Added %s to region %s" % (c.shortname, region.name)
