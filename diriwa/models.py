from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
	name		= models.CharField(max_length=200)


class Entry(models.Model):
	pass


class RegionalEntity(Entry):
	name		= models.CharField(max_length=200)
	shortname	= models.CharField(max_length=70, blank=True)
	isocode		= models.CharField(max_length=3, blank=True)
	map			= models.FileField(upload_to="static/img/maps/", blank=True)

	class Meta:
		ordering	= ["shortname"]


class Region(RegionalEntity):
	union		= models.BooleanField(default=False)
	
	class Meta:
		ordering	= ["name"]
		
	def population(self):
		return sum([x.population for x in self.country_set.all()])
		
	def __unicode__(self):
		return self.name



class RegionalEntityLocalName(models.Model):
	language		= models.ForeignKey(Language)
	entity		= models.ForeignKey(RegionalEntity)
	name		= models.CharField(max_length=200, blank=True)


class Country(RegionalEntity):
	population	= models.IntegerField(blank=True, default=0)
	regions		= models.ManyToManyField(Region)
	languages	= models.ManyToManyField(Language)
	
	
	def safe(self):
		if self.shortname == "":
			self.shortname = self.name
		super(self, save)()
		
	
	def longname(self):
		return not (self.name == self.shortname)
	
	def __unicode__(self):
		return self.shortname


class Topic(Entry):
	name		= models.CharField(max_length=100)
	
	class Meta:
		ordering	= ["name"]
		

class EntityTopic(Entry):
	country		= models.ForeignKey(RegionalEntity)
	topic		= models.ForeignKey(Topic)
	text			= models.TextField()


class Tag(models.Model):
	name		= models.CharField(max_length = 40)
	description	= models.TextField()


class EntityTag(models.Model):
	pass
	

class CourtCase(Entry):
	country		= models.ForeignKey(RegionalEntity)
	
	
class NewsItem(models.Model):
	headline		= models.CharField(max_length=200)
	text			= models.TextField()
	itemref		= models.ForeignKey(Entry, blank=True, null=True)
	author		= models.ForeignKey(User)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited		= models.DateTimeField(auto_now=True)


class Link(models.Model):
	title					= models.CharField(max_length=200)
	url					= models.URLField()
	description			= models.TextField()
	itemref				= models.ForeignKey(Entry, blank=True, null=True)
	author				= models.ForeignKey(User)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited		= models.DateTimeField(auto_now=True)
	
	
