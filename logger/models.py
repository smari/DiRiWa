from django.db import models


class EventType(models.Model):
	"""
		Event classifications for the log.
	"""
	name			= models.CharField(max_length=60)
	show_default		= models.BooleanField()
	metadata_fields	= JSONField()

	def __unicode__(self):
		return self.name


class EventLog(models.Model):
	"""
		The event log.
	"""
	user			= models.ForeignKey(User, blank=True, null=True)
	timestamp	= models.DateTimeField(auto_now=True)
	text			= models.CharField(max_length=300)
	type			= models.ForeignKey(EventType)

	def __unicode__(self):
		return "[%-15s]-[%s] %s (%s)" % (self.type, self.timestamp, self.text, self.user)


