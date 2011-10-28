from diriwa.models import *

def menucontext(request):
	ctx = {}
	ctx["menu_regions"] = Region.objects.filter(type__in_menu=True)
	ctx["menu_topics"] = Topic.objects.filter()

	return ctx
