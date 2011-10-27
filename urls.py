from django.conf.urls.defaults import *
from django.views.generic import ListView, TemplateView

from diriwa.views import *

urlpatterns = patterns('',
	(r"^$",									TemplateView.as_view(template_name="index.html")),
	(r"^about/credits/$",						TemplateView.as_view(template_name="credits.html")),
	(r"^about/$",								TemplateView.as_view(template_name="about.html")),
	(r"^tags/$",								ListView.as_view(model=Tag)),
	(r"^regions/$",							ListView.as_view(model=Region, context_object_name="regions")),
	(r"^regions/region/(?P<pk>\d+)/$",			RegionView.as_view()),
	(r"^countries/$",							ListView.as_view(model=Country, context_object_name="countries")),
	(r"^countries/country/(?P<pk>\d+)/$",		CountryView.as_view()),
)

urlpatterns += patterns('',
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
