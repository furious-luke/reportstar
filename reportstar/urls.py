from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^ready/(?P<runid>[a-zA-Z0-9]+)/$', 'reportstar.views.index'),
    url(r'^complete$', TemplateView.as_view(template_name='complete.html')),
    url(r'^emailer/(?P<qname>[a-zA-Z0-9_]+)/$', 'questionnaire.emails.send_emails'),
    url(r'q/', include('questionnaire.urls')),
    url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    # url(r'^$', 'questionnaire.page.views.page', {'page' : 'index'}),
    url(r'^(?P<page>.*)\.html$', 'questionnaire.page.views.page'),
    url(r'^(?P<lang>..)/(?P<page>.*)\.html$', 'questionnaire.page.views.langpage'),
    url(r'^setlang/$', 'questionnaire.views.set_language'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
