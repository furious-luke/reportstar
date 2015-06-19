from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'green2.views.select_questionnaire'),
    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^ready/(?P<runid>[a-zA-Z0-9]+)/$', 'green2.views.index'),
    url(r'^complete/$', TemplateView.as_view(template_name='complete.html')),
    # url(r'^emailer/(?P<qname>[a-zA-Z0-9_]+)/$', 'questionnaire.emails.send_emails'),
    url(r'q/', include('questionnaire.urls')),
    # url(r'^take/(?P<questionnaire_id>[0-9]+)/$', 'questionnaire.views.generate_run'),
    # url(r'^$', 'questionnaire.page.views.page', {'page' : 'index'}),
    # url(r'^(?P<page>.*)\.html$', 'questionnaire.page.views.page'),
    url(r'^(?P<lang>..)/(?P<page>.*)\.html$', 'questionnaire.page.views.langpage'),
    url(r'^setlang/$', 'questionnaire.views.set_language'),
    url(r'^emailer/$', 'green2.views.select_questionnaire'),
    url(r'^emailer/subjects/$', 'green2.views.select_subjects', name="email_subj"),
    url(r'^emailer/go/$', 'green2.views.email', name="email_go"),
    url(r'^document/(?P<proj_id>[a-zA-Z0-9_]+)/(?P<year>[0-9]+)/$', 'green2.views.document', name='document'),
    url(r'^logos$', 'green2.views.logos', name='logos'),
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]
