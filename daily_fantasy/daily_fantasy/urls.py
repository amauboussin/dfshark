from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'global_lobby.views.home', name='home'),
    url(r'rawdata$', 'global_lobby.views.raw_data', name='data'),
    url(r'print', 'global_lobby.views.print_contests', name='print'),
    url(r'refresh', 'global_lobby.views.refresh_database', name='refresh'),
    url(r'test', 'global_lobby.views.test_scraper', name='test'),
    # url(r'^daily_fantasy/', include('daily_fantasy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
