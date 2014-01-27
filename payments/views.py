from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django_tables2 import SingleTableView
from payments.forms import AddPaymentForm
from payments.models import Corporation, Payment
from payments.tables import PaymentsTable, PaymentsPartialTable

# from django.utils.datetime_safe import datetime

# Create your views here.


def index(request):
    return render(request, 'payments/index.html')


def register(request):
    return render(request, 'payments/register.html')


@login_required
def after_login(request):
    username = request.user.username
    return HttpResponseRedirect(reverse_lazy('home',
        kwargs={'username': username})
    )


class HomeView(SingleTableView):

    model = Payment
    template_name = 'payments/home.html'
    table_class = PaymentsPartialTable

    def __init__(self, user=None, *args, **kwargs):
        super(HomeView, self).__init__(*args, **kwargs)
        self._user = user

    def get_context_data(self, **kwargs):
        """ Adds tables of late and near due payments to the context
        """
        # filter overview payments
        context = super(HomeView, self).get_context_data(**kwargs)
        late_payments_data = \
            Payment.objects.filter(due_date__lt=datetime.today)
        context['table'] = PaymentsPartialTable(late_payments_data)
        # filter payments due in 6 days
        startdate = datetime.today()
        enddate = startdate + timedelta(days=6)
        neardue_payments_data = \
            Payment.objects.filter(due_date__range=[startdate, enddate])
        context['table_neardue_payments'] = \
            PaymentsPartialTable(neardue_payments_data)
        return context

    def get_queryset(self):
        return self.request.user.payments.all()

    """This is how you decorate class see:
       https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


@login_required
def statistics(request, username):
    return render(request, 'payments/statistics.html', {'username': username})


@login_required
def settings(request, username):
    return render(request, 'payments/settings.html', {'username': username})


# login_required
class PaymentsList(SingleTableView):
    model = Payment
    template_name = 'payments/payments.html'
    table_class = PaymentsTable

    def get_queryset(self):
        return Payment.objects.filter(owner=self.request.user)

    """This is how you decorate class see:
       https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    """
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentsList, self).dispatch(*args, **kwargs)


# login_required
class PaymentCreate(CreateView):

    model = Payment
    success_url = reverse_lazy('search')
    form_class = AddPaymentForm
    fields = ('corporation',
            'title',
            'amount',
            'due_date',
            'supply_date',
            'pay_date'
    )

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.owner = self.request.user
        return super(PaymentCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('payments', kwargs={'username': self.request.user})

    """This is how you decorate class see:
       https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentCreate, self).dispatch(*args, **kwargs)


def search(request):
            # name__icontains=request.POST['search_term'])
    return HttpResponseRedirect(reverse_lazy('corporation',
        kwargs={'corporation': request.GET['search_term'.encode('utf-8')]})
                                # request.POST.get('corporation_name')
    )


def corporation_detail(request, corporation):
    obj = get_object_or_404(Corporation,
            name__icontains=corporation)
    return render(request, 'payments/company.html', {'corporation': obj})


# class CorporationView(DetailView):
#     model = Corporation
#     template_name = 'payments/company.html'
#     # context_object_name = 'corporation'
#
#     def get_object(self, *args, **kwargs):
#         return get_object_or_404(Corporation,
#             name__icontains=kwargs['pk'])
