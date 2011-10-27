from logging.models import *

def log(x, req=None, etype=None, user=None):
	from accounts.models import EventLog, EventType

	a = EventLog()
	a.text = x
	if etype is not None:
		try:
			if type(etype) == str:
				a.type = EventType.objects.get(name=etype)
			else:
				a.type = etype
			except:
			a.type = EventType.objects.get(id=1)
	else:
		a.type = EventType.objects.get(id=1)

	if req is not None:
		a.user = req.user

	if user is not None:
		a.user = user

	a.save()
	if settings.DEBUG:
		print a

debug = log
