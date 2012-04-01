from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext as _
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q

from django.views.generic import TemplateView, DetailView, CreateView, UpdateView

from datetime import datetime, timedelta, date
import settings

from diriwa.models import *
from diriwa.forms import *

import simplejson as json


def jsonize(f):
	def wrapped(*args, **kwargs):
		return HttpResponse(json.dumps(f(*args, **kwargs)))

	return wrapped





class RegionDetailView(DetailView):
	context_object_name = "region"
	model = Region

	
class CountryDetailView(DetailView):
	context_object_name = "country"
	model = Country


class TopicDetailView(DetailView):
	context_object_name = "topic"
	model = Topic


class SectionCreateView(CreateView):
	context_object_name = "section"
	template_name = "diriwa/entitytopic_new.html"
	form_class = SectionForm
	success_url = "/regions/region/%(country)d/"


class SectionDetailView(DetailView):
	context_object_name = "section"
	model = EntityTopic



@login_required
@jsonize
def section_vote(request):
	ctx = {"ok": True}

	user = request.user
	section = request.REQUEST.get("section", 0)
	vote = int(request.REQUEST.get("vote", 5))

	if section == 0:
		return {"ok": False, "error": "Invalid section (zero)"}

	try:
		v, created = EntityTopicVote.objects.get_or_create(user=user, section_id=section)
	except Exception, e:
		return {"ok": False, "error": "Invalid section (%s)" % e}
		
	v.value = vote
	v.save()

	ctx["section"] = section
	ctx["vote"] = vote
	ctx["user"] = user.username
	ctx["severity"] = v.section.severity()
	ctx["votes"] = v.section.votes()
	
	return ctx

