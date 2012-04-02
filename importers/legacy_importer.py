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

csvfile = open("../data/legacy-pages.csv")
# dialect = csv.Sniffer().sniff(csvfile.read(1024))
# csvfile.seek(0)
reader = csv.reader(csvfile, dialect=csv.excel)
headers = reader.next()

for line in reader:
	# print line
	# print "Entity: %s  -  Subject: %s" % (line[0], line[1])
	try:
		region = Region.objects.get(name__iequals=line[0])
	except:
		try:
			region = Region.objects.get(shortname__iequals=line[0])
		except:
			try:
				region = Region.objects.get(name__icontains=line[0])
			except:
				try:
					region = Region.objects.get(shortname__icontains=line[0])
				except:
					print "Dunno what to do with '%s'" % line[0]
					continue

	topic, created = Topic.objects.get_or_create(name=line[1])
	if created:
		print "Created new topic %s" % topic.name
	s, screated = Section.objects.get_or_create(region=region, topic=topic)
	s.text = line[2]
	s.save()
	# print "Using region '%s' for '%s" % (region, line[0])
	if screated:
		print "Imported new section '%s' for '%s'" % (topic.name, region)
	else:
		print "Update section '%s' for '%s'" % (topic.name, region)
