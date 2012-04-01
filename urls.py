from django.conf.urls.defaults import *
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required

from diriwa.views import *
from diriwa.forms import *

urlpatterns = patterns('',
	(r"^$",					TemplateView.as_view(template_name="index.html")),
	(r"^about/credits/$",			TemplateView.as_view(template_name="credits.html")),
	(r"^about/$",				TemplateView.as_view(template_name="about.html")),
	(r"^news/$",				ListView.as_view(model=NewsItem, context_object_name="newsitems")),
	(r"^news/(?P<pk>\d+)/$",		DetailView.as_view(model=NewsItem, context_object_name="newsitems")),
	(r"^tags/$",				ListView.as_view(model=Tag, context_object_name="tags")),
	(r"^regions/$",				ListView.as_view(model=Region, context_object_name="regions")),
	(r"^regions/add/$",			login_required(CreateView.as_view(model=Region, success_url="/regions/region/%(id)d/", template_name_suffix="_new"))),
	(r"^regions/edit/(?P<pk>\d+)/$",	login_required(UpdateView.as_view(model=Region, success_url="/regions/region/%(id)d/", template_name_suffix="_edit"))),
	(r"^regions/region/(?P<pk>\d+)/$",	RegionView.as_view()),
	(r"^countries/$",			ListView.as_view(model=Country, context_object_name="countries")),
	(r"^countries/add/$",			login_required(CreateView.as_view(model=Country, success_url="/countries/country/%(id)d/", template_name_suffix="_new"))),
	(r"^countries/edit/(?P<pk>\d+)/$",	login_required(UpdateView.as_view(model=Country, success_url="/countries/country/%(id)d/", template_name_suffix="_edit"))),
	(r"^countries/country/(?P<pk>\d+)/$",	CountryView.as_view()),
	(r"^topics/$",				ListView.as_view(model=Topic, context_object_name="topics")),
	(r"^topics/add/$",			login_required(CreateView.as_view(model=Topic, success_url="/topics/topic/%(id)d/", template_name_suffix="_new"))),
	(r"^topics/edit/(?P<pk>\d+)/$",		login_required(UpdateView.as_view(model=Topic, success_url="/topics/topic/%(id)d/", template_name_suffix="_edit"))),
	(r"^topics/topic/(?P<pk>\d+)/$",	TopicView.as_view()),
	(r"^sections/$",			ListView.as_view(model=EntityTopic, context_object_name="sections")),
	(r"^sections/add/$",			login_required(CreateView.as_view(model=EntityTopic, success_url="/sections/section/%(id)d/", template_name_suffix="_new"))),
	(r"^sections/edit/(?P<pk>\d+)/$",	login_required(UpdateView.as_view(model=EntityTopic, success_url="/sections/section/%(id)d/", template_name_suffix="_edit"))),
	(r"^sections/section/(?P<pk>\d+)/$",	SectionView.as_view()),
	(r"^sections/vote/$",			"diriwa.views.section_vote"),		
	(r'^accounts/profile/',			TemplateView.as_view(template_name="registration/profile.html")),
	(r'^accounts/',				include('registration.urls')),
)

urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
