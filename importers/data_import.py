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
import settings
settings.DEBUG = False

csvfile = open("../data/countrylist.csv")
dialect = csv.Sniffer().sniff(csvfile.read(1024))
csvfile.seek(0)
reader = csv.reader(csvfile, dialect=dialect)
headers = reader.next()

#   0		1	2			3		4		  5   6    7		  8 	 9 	 10	11	12    13     14
# ['7', 'Argentina', 'Argentine Republic', 'South America', 'Independent State', '', '', 'Buenos Aires', 'ARS', 'Peso', '+54', 'AR', 'ARG', '032', '.ar']

georegion, created = RegionType.objects.get_or_create(name="Geographic region", in_menu=True)
union, created = RegionType.objects.get_or_create(name="Union")
treaty, created = RegionType.objects.get_or_create(name="Treaty")
bloc, created = RegionType.objects.get_or_create(name="Block")
country, created = RegionType.objects.get_or_create(name="Country")

for line in reader:
	c, created = Country.objects.get_or_create(shortname=line[1], name=line[2], type=country)
	c.isocode = line[11]
	c.currency = line[9]
	c.capital = line[7]
	c.deptype = line[4]
	c.depsubtype = line[5]
	c.itu_t = line[10]
	c.tld = line[14]
	c.save()
	if created:
		print "Created country %s" % c.shortname
	else:
		print "Updated country %s" % c.shortname

	region, created = Region.objects.get_or_create(name=line[3], type=georegion)
	c.regions.add(region)
	if created:
		print "Created new %s: %s" % (region.type.name, region.name)

	if line[6] != '':
		parent, created = Country.objects.get_or_create(shortname=line[6], type=country)
		c.regions.add(parent)

