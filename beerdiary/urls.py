
from django.conf.urls.defaults import *
from django.contrib import admin
import os
from user_management.views import *

admin.autodiscover()


urlpatterns = patterns('',
    (r'^$', 'browsing_app.views.home'),
    (r'^login/$', 'user_management.views.login_user'),
    (r'^logout/$', 'user_management.views.logout_user'),
    (r'^create/$', create_user),

    (r'^create_done/$', create_user_done),
    (r'^profile/$', user_profile),
    (r'^profile/edit$', user_profile_edit),

    (r'^site_media/(.*)$', 'django.views.static.serve', {'document_root': os.path.join(os.path.dirname(__file__), 'site_media')}),

    # gdy jest podane *_id to wyswietlamy odpowiednia stronke danego piwa/browaru/panstwa
    # w przeciwnym razie dajemy liste wszystkich
    (r'^tag/(?P<tag_name>\w*)$', 'browsing_app.views.tag_view'),

    (r'^beer/(?P<beer_id>\d*)/add_review$', 'browsing_app.views.add_review'),
    (r'^beer/(?P<beer_id>\d*)', 'browsing_app.views.beer_view'),


    (r'^brewery/(?P<brewery_id>\d*)$', 'browsing_app.views.brewery_view'),

    (r'^country/(?P<country_id>\d*)$', 'browsing_app.views.country_view'),

    (r'^admin/', include(admin.site.urls)),

    (r'^news/$', 'browsing_app.views.news_view'),
    (r'^search/$', 'browsing_app.views.search_view'),
    (r'^contact/$', 'messages.views.message_view'),
    (r'^contact/sent/$', 'messages.views.message_sent_view'),
    (r'^report/(?P<id>\d*)$', 'messages.views.report'),

    (r'^recommendation/$', 'recommendation.views.get_recommendation'),

    (r'^moderator/$', 'moderators_panel.views.moderator_view'),

    (r'^access_denied/$','moderators_panel.views.access_denied'),
    (r'^moderator/beer/edit/(?P<id>\d*)$', 'moderators_panel.views.beer_edit'),
    (r'^moderator/beer/del/(?P<id>\d*)$', 'moderators_panel.views.beer_delete'),
    (r'^moderator/beer/add/(?P<id>\d*)$', 'moderators_panel.views.beer_add'),

    (r'^moderator/brewery/edit/(?P<id>\d*)$', 'moderators_panel.views.brewery_edit'),
    (r'^moderator/brewery/del/(?P<id>\d*)$', 'moderators_panel.views.brewery_delete'),
    (r'^moderator/brewery/add/(?P<id>\d*)$', 'moderators_panel.views.brewery_add'),

    (r'^moderator/country/edit/(?P<id>\d*)$', 'moderators_panel.views.country_edit'),
    (r'^moderator/country/del/(?P<id>\d*)$', 'moderators_panel.views.country_delete'),
    (r'^moderator/country/add/$', 'moderators_panel.views.country_add'),

    (r'^moderator/message/$', 'moderators_panel.views.message_view'),
    (r'^moderator/message/del/(?P<id>\d*)$', 'moderators_panel.views.delete_message'),

)
    # Examples:
    # url(r'^$', 'beerdiary.views.home', name='home'),
    # url(r'^beerdiary/', include('beerdiary.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
