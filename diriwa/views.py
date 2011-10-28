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

from django.views.generic import TemplateView, DetailView

from datetime import datetime, timedelta, date
import settings

from diriwa.models import *
from diriwa.forms import *


class RegionView(DetailView):
	context_object_name = "region"
	model = Region

	
class CountryView(DetailView):
	context_object_name = "country"
	model = Country


class TopicView(DetailView):
	context_object_name = "topic"
	model = Topic


class SectionView(DetailView):
	context_object_name = "section"
	model = EntityTopic
	
