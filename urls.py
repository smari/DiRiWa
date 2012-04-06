from django.conf.urls.defaults import *
from django.views.generic import ListView, TemplateView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib import admin

from diriwa.views import *
from diriwa.forms import *

admin.autodiscover()

urlpatterns = patterns('',
	(r"^$",						TemplateView.as_view(template_name="index.html")),
	(r"^about/credits/$",				TemplateView.as_view(template_name="credits.html")),
	(r"^about/$",					TemplateView.as_view(template_name="about.html")),

	(r"^news/$",					ListView.as_view(model=NewsItem, context_object_name="newsitems")),
	(r"^news/add/$",				login_required(NewsItemCreateView.as_view())),
	(r"^news/(?P<pk>\d+)/$",			DetailView.as_view(model=NewsItem, context_object_name="newsitems")),

	(r"^tags/$",					ListView.as_view(model=Tag, context_object_name="tags")),

	(r"^regions/$",					ListView.as_view(model=Region, context_object_name="regions")),
	(r"^regions/add/$",				login_required(CreateView.as_view(model=Region, success_url="/regions/%(id)d/", template_name_suffix="_new"))),
	(r"^regions/edit/(?P<pk>\d+)/$",		login_required(UpdateView.as_view(model=Region, success_url="/regions/%(id)d/", template_name_suffix="_edit"))),
	(r"^regions/(?P<pk>\d+)/$",			RegionDetailView.as_view()),
	(r"^regions/(?P<region>\d+)/sections/add/$",	login_required(SectionCreateView.as_view())),
	(r"^regions/(?P<entity>\d+)/news/add/",		login_required(NewsItemCreateView.as_view())),

	(r"^entities/(?P<entity>\d+)/news/add/",	login_required(NewsItemCreateView.as_view())),
	#(r"^regions/(?P<region>\d+)/links/add/",	login_required(LinkCreateView.as_view())),
	#(r"^regions/(?P<region>\d+)/memberships/edit/",	login_required(MembershipUpdateView.as_view())),

	(r"^topics/$",					ListView.as_view(model=Topic, context_object_name="topics")),
	(r"^topics/add/$",				login_required(CreateView.as_view(model=Topic, success_url="/topics/%(id)d/", template_name_suffix="_new"))),
	(r"^topics/edit/(?P<pk>\d+)/$",			login_required(UpdateView.as_view(model=Topic, success_url="/topics/%(id)d/", template_name_suffix="_edit"))),
	(r"^topics/(?P<pk>\d+)/$",			TopicDetailView.as_view()),

	(r"^sections/$",				ListView.as_view(model=Section, context_object_name="sections")),
	(r"^sections/edit/(?P<pk>\d+)/$",		login_required(UpdateView.as_view(model=Section, success_url="/sections/%(id)d/", template_name_suffix="_edit"))),
	(r"^sections/(?P<pk>\d+)/$",			SectionDetailView.as_view()),
	(r"^sections/vote/$",				"diriwa.views.section_vote"),		

	(r'^accounts/profile/',				TemplateView.as_view(template_name="registration/profile.html")),
	(r'^accounts/',					include('registration.urls')),
   url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
