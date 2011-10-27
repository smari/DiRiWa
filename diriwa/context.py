from diriwa.models import *

def menucontext(request):
	ctx = {}
	ctx["menu_regions"] = Region.objects.filter(union=False)
	ctx["menu_topics"] = Topic.objects.filter() # parent=None)

	return ctx
