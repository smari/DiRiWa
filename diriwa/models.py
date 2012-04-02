from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
	name		= models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Entity(models.Model):
	pass
		

class RegionType(models.Model):
	name		= models.CharField(max_length=50)
	in_menu		= models.BooleanField(default=False)
	
	def __unicode__(self):
		return self.name


class Region(Entity):
	name			= models.CharField(max_length=200)
	shortname		= models.CharField(max_length=70, blank=True)
	isocode			= models.CharField(max_length=3, blank=True)
	map			= models.FileField(upload_to="static/img/maps/", blank=True)
	type			= models.ForeignKey(RegionType)
	population		= models.IntegerField(blank=True, default=0)
	url			= models.URLField(blank=True, null=True)
	tld			= models.CharField(max_length=20, blank=True, null=True)
	itu_t			= models.CharField(max_length=20, blank=True, null=True)
	deptype			= models.CharField(max_length=50, blank=True, null=True)
	depsubtype		= models.CharField(max_length=50, blank=True, null=True)
	capital			= models.CharField(max_length=100, blank=True, null=True)
	currency		= models.CharField(max_length=100, blank=True, null=True)
	languages		= models.ManyToManyField(Language, blank=True)
	regionmembers		= models.ManyToManyField("Region", blank=True, through="RegionMembership")

	class Meta:
		ordering	= ["name", "shortname", "type"]

	def safe(self):
		if self.shortname == "":
			self.shortname = self.name
		super(self, save)()
	
	def longname(self):
		return not (self.name == self.shortname)
		
	def treaties(self):
		return self.member_of.filter(region__type__name="Treaty")

	def unions(self):
		return self.member_of.filter(region__type__name="Union")

	def geographical(self):
		return self.member_of.filter(region__type__name__in=["Block", "Geographic region", "Country"])

	def __unicode__(self):
		return self.shortname
	
	def get_population(self):
		return sum([x.member.population for x in self.regionmembers.all()])
			
	def agreements(self):
		agreements = []
		for i in self.regionmembers.all():
			agreements.extend([x.region for x in i.treaties()])
			agreements.extend([x.region for x in i.unions()])
		return set(agreements)
		
	def __unicode__(self):
		return self.name			


class RegionLocalName(models.Model):
	language	= models.ForeignKey(Language)
	region		= models.ForeignKey(Region)
	name		= models.CharField(max_length=200, blank=True)



class RegionMembership(models.Model):
	region		= models.ForeignKey(Region, related_name="members")
	member		= models.ForeignKey(Region, related_name="member_of")
	type		= models.CharField(max_length=100, blank=True, null=True)

	def __unicode__(self):
		return "%s member of %s (%s)" % (self.member, self.region, self.type)


class Topic(Entity):
	name			= models.CharField(max_length=100)
	
	class Meta:
		ordering	= ["name"]
		
	def __unicode__(self):
		return self.name

class Section(Entity):
	region			= models.ForeignKey(Region)
	topic			= models.ForeignKey(Topic)
	text			= models.TextField()
	

	def wikitext(self):
		from mwlib.uparser import simpleparse
		from htmlwriter import HTMLWriter
		from StringIO import StringIO
		out = StringIO()
		print "Unwikified text: %s" % (self.text)
		w = HTMLWriter(out)
		w.write(simpleparse(self.text))
		return out.getvalue()


	def severity(self):
		votes = self.sectionvote_set.all()
		count = votes.count()
		if count == 0:
			return 1
		return sum([x.value for x in votes])/count # Simple average


	def votes(self):
		return self.sectionvote_set.all().count()
		
	
	class Meta:
		unique_together	=	(("region", "topic"),)


class SectionVote(models.Model):
	section			= models.ForeignKey(Section)
	user			= models.ForeignKey(User)
	value			= models.IntegerField(default=1)

	class Meta:
		unique_together	=	(("section", "user"),)


class Tag(models.Model):
	name			= models.CharField(max_length = 40)
	description		= models.TextField()


class EntityTag(models.Model):
	tag			= models.ForeignKey(Tag)
	entity			= models.ForeignKey(Entity)
	value			= models.CharField(max_length=100, null=True, blank=True)


class CourtCase(Entity):
	region			= models.ForeignKey(Region)
	# Not done
	
	
class NewsItem(models.Model):
	headline		= models.CharField(max_length=200)
	text			= models.TextField()
	itemref			= models.ForeignKey(Entity, blank=True, null=True)
	author			= models.ForeignKey(User)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited	= models.DateTimeField(auto_now=True)


class Link(models.Model):
	title			= models.CharField(max_length=200)
	url			= models.URLField()
	description		= models.TextField()
	itemref			= models.ForeignKey(Entity, blank=True, null=True)
	author			= models.ForeignKey(User)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited	= models.DateTimeField(auto_now=True)
	
	
