from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from payments.views import index, home, statistics, settings, register, search


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'musar.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index, name='index'),

    url(r'^register/$',
        register, name='register'),

    url(r'^search/$',
        search, name='search'),

    url(r'^user/(?P<username>\w+)/$',
        login_required(home), name='home'),

    url(r'^user/(?P<username>\w+)/statistics/$',
        statistics, name='statistics'),

    url(r'^user/(?P<username>\w+)/settings/$',
        login_required(settings), name='settings'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name="login"),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('index')}, name="logout"),

    url(r'^admin/', include(admin.site.urls)),

)
