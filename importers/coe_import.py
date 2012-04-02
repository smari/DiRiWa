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

csvfile = open("../data/coe_conventions.csv")
dialect = csv.Sniffer().sniff(csvfile.read(4096))
csvfile.seek(0)
reader = csv.reader(csvfile, dialect=dialect)
headers = reader.next()

# Country,Ratification,treaty,Entry,Signature,Note,Territorial Application,Declarations,Reservations,Communication,Authorities,Denunciation,Effect denunciation,Objection
# Slovakia,18/3/1992,Convention for the Protection of Human Rights and Fundamental Freedoms,1/1/1993,21/2/1991,17,,X,X,,,,,

treatytype, created = RegionType.objects.get_or_create(name="Treaty")

for line in reader:
	treaty, created = Region.objects.get_or_create(name=line[2], type=treatytype)

	if created:
		print "Created treaty %s" % treaty.name

	try:	signatory = Region.objects.get(name=line[0])
	except:
		try:	signatory = Region.objects.get(shortname=line[0])
		except:
			print "Failed to recognize signatory '%s'" % line[0]
			continue

	# print signatory
	if line[1]:
		memrel, created = RegionMembership.objects.get_or_create(region=treaty, member=signatory)
		memrel.type = "Ratified"
		memrel.save()
		if created:
			print "Added %s to treaty %s" % (signatory, treaty.name)
