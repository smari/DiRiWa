from django.db import models
from django.contrib.auth.models import User


class Language(models.Model):
	name		= models.CharField(max_length=200)

	def __unicode__(self):
		return self.name


class Triple(models.Model):
        entity          = models.ForeignKey("Entity")
        key             = models.CharField(max_length=200)
        value           = models.CharField(max_length=200)

        # <entity, "memopol", "http://...">
        
        def __unicode__(self):
                return u"(%d, '%s', '%s')" % (self.entity.id, self.key, self.value)
        
        class Meta:
                ordering  = ["entity", "key"]

class Entity(models.Model):
        pass

	def triple_get(self, key, default=None):
                try:
                        return self.triple_set.get(key=key).value
                except DoesNotExist:
                        return default

        def triple_setval(self, key, value):
                t, created = self.triple_set.get_or_create(key=key)
                t.value = value
                t.save()
                return t

        set_triple = triple_setval
        get_triple = triple_get

        def triple_delete(self, key):
                try:
                        t = self.triple_set.get(key=key)
                        t.delete()
                except DoesNotExist:
                        # If it doesn't exist, we succeded, eh?
                        return True

        def triple_list(self):
                return [x.key for x in self.triple_set.all()]

        def triple_dict(self):
                d = {}
                for item in self.triple_set.all():
                        d[item.key] = item.value

                return d

        def triple_triples(self):
                l = []
                for item in self.triple_set.all():
                        l.append((item.entity, item.key, item.value))

        def triple_rdf(self):
                # TODO: Fix this to show actual RDF output.
                t = "<triples>\n"
                for item in self.triple_set.all():
                        t += "  <triple>\n"
                        t += "    <entity id=\"%d\"/>\n" % item.entity.id
                        t += "    <key>%s</key>\n" % item.key
                        t += "    <value>%s</key>\n" % item.value
                        t += "  </triple>\n"
                t += "</triples>\n"
                return t

        def triple_json(self):
                return {"entity": self.id, "dict": self.triple_dict()}
        

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
        description             = models.TextField(default='')

	class Meta:
		ordering	= ["name", "shortname", "type"]

	def safe(self):
		if self.shortname == "":
			self.shortname = self.name
		super(self, save)()

        def get_name(self):
                if self.shortname != "":
                        return self.shortname
                return self.name
	
	def longname(self):
		return not (self.name == self.shortname)
		
	def treaties(self):
		return self.member_of.filter(region__type__name="Treaty")

	def unions(self):
		return self.member_of.filter(region__type__name="Union")

	def geographical(self):
		return self.member_of.filter(region__type__name__in=["Block", "Geographic region", "Country"])
	
	def get_population(self):
                if self.population > 0:
                        return population
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


class SectionHistory(models.Model):
        entity                  = models.ForeignKey(Entity)
        oldtext                 = models.TextField()
        timestamp               = models.DateTimeField(auto_now=True)
        user                    = models.ForeignKey(User, blank=True, null=True)

        class Meta:
                ordering = ["-timestamp"]


class Section(Entity):
	region			= models.ForeignKey(Region)
	topic			= models.ForeignKey(Topic)
        user                    = models.ForeignKey(User, null=True, blank=True)
	text			= models.TextField()
        
        
        def save(self, *args, **kwargs):
                super(Section, self).save(*args, **kwargs)
                s = SectionHistory(entity=self, oldtext=self.text, user=self.user)
                s.save()

        def history(self):
                return SectionHistory.objects.filter(entity=self)

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
	url			= models.URLField()
	itemref			= models.ForeignKey(Entity, blank=True, null=True)
	author			= models.ForeignKey(User)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited	= models.DateTimeField(auto_now=True)


class Link(models.Model):
	title			= models.CharField(max_length=200)
	url			= models.URLField()
	description		= models.TextField()
	itemref			= models.ForeignKey(Entity, blank=True, null=True)
	author			= models.ForeignKey(User, blank=True, null=True)
	timestamp_submitted	= models.DateTimeField(auto_now_add=True)
	timestamp_edited	= models.DateTimeField(auto_now=True)
	
	
