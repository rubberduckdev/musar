from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import TemplateView
from payments.views import (
    index, HomeView, PaymentCreate, statistics,
    settings, register, search, after_login, PaymentsList, corporation_detail,
    LoadPaymentsFileView, PaymentsFileView, load_payments_from_file_view,
    AddPaymentsList, save_payments_list_view,
)


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
        HomeView.as_view(), name='home'),

    url(r'^user/(?P<username>\w+)/payments/$',
        login_required(PaymentsList.as_view()),
        name='payments'),

    url(r'^user/(?P<username>\w+)/statistics/$',
        statistics, name='statistics'),

    url(r'^user/(?P<username>\w+)/settings/$',
        login_required(settings), name='settings'),

    url(r'^corporation/(?P<corporation>\w+)/$',
        corporation_detail, name='corporation'),

    url(r'^user/new/$',
        TemplateView.as_view(template_name="payments/new_account.html"),
        name='new_account'),

    url(r'^login/$',
        'django.contrib.auth.views.login',
        {'template_name': 'login.html'},
        name="login"),

    url(r'^accounts/profile/$', login_required(after_login)),

    url(r'^logout/$',
        'django.contrib.auth.views.logout',
        {'next_page': reverse_lazy('index')}, name="logout"),

    url(r'^company/$',
        TemplateView.as_view(template_name="payments/company.html"),
        name='company'),

#    url(r'^user/(?P<username>\w+)/add_payments/$',
#        login_required(TemplateView.as_view(
#            template_name="payments/add_payments.html")),
#        name='add_payments'),

    url(r'^user/(?P<username>\w+)/add_payments/$',
        PaymentCreate.as_view(),
        name='add_payments'),

    url(r'^user/(?P<username>\w+)/add_payments_file/$',
        load_payments_from_file_view,
        name='add_payments_file'),

    url(r'^user/(?P<username>\w+)/add_payments_list/$',
        AddPaymentsList.as_view(),
        name='add_payments_list'),

    url(r'^user/(?P<username>\w+)/save_payments_file/$',
        save_payments_list_view,
        name='save_payments_file'),

    url(r'^file/$',
        PaymentsFileView.as_view(),
        name='file'),

    url(r'^admin/', include(admin.site.urls)),


)
