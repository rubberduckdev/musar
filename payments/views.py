from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.http import request
from django.shortcuts import render_to_response
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
#from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
#from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, FormView
from django_tables2 import SingleTableView
from payments.forms import AddPaymentForm, LoadFileForm
from payments.models import Corporation, Payment
from payments.tables import PaymentsTable, PaymentsPartialTable
#from django.core.files.uploadedfile import SimpleUploadedFile
from django.template import RequestContext
#import csv
import logging
#from payments.csv_models import PaymentCsvModel
from django.http import HttpResponseNotFound


# Get an instance of a logger
logger = logging.getLogger(__name__)
# from django.utils.datetime_safe import datetime

# Create your views here.


def index(a_request):
    return render(a_request, 'payments/index.html')


def register(a_request):
    return render(a_request, 'payments/register.html')


@login_required
def after_login(a_request):
    username = a_request.user.username
    return HttpResponseRedirect(
        reverse_lazy('home', kwargs={'username': username}))


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
        late_payments_data = Payment.objects.filter(
            due_date__lt=datetime.today)
        context['table'] = PaymentsPartialTable(late_payments_data)
        # filter payments due in 6 days
        startdate = datetime.today()
        enddate = startdate + timedelta(days=6)
        neardue_payments_data = Payment.objects.filter(
            due_date__range=[startdate, enddate])
        context['table_neardue_payments'] = PaymentsPartialTable(
            neardue_payments_data)
        return context

    def get_queryset(self):
        return self.request.user.payments.all()

    #  This is how you decorate class see:
    #  https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)


@login_required
def statistics(a_request, username):
    return render(a_request, 'payments/statistics.html', {'username': username})


@login_required
def settings(a_request, username):
    return render(a_request, 'payments/settings.html', {'username': username})


# login_required
class PaymentsList(SingleTableView):
    model = Payment
    template_name = 'payments/payments.html'
    table_class = PaymentsTable

    def get_queryset(self):
        return Payment.objects.filter(owner=self.request.user)

    # This is how you decorate class see:
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentsList, self).dispatch(*args, **kwargs)


class AddPaymentsList(SingleTableView):
    model = Payment
    template_name = 'payments/payments.html'
    table_class = PaymentsTable

    def __init__(self, *args, **kwargs):
        super(AddPaymentsList, self).__init__(*args, **kwargs)
        self.csv_payments = kwargs['payments']

    def get_queryset(self):
        return self.csv_payments

    # This is how you decorate class see:
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentsList, self).dispatch(*args, **kwargs)


def load_payments_from_file_view(a_request, username):
    if a_request.method == 'POST':
        payments = []
        form = LoadFileForm(a_request.POST, a_request.FILES)
        if form.is_valid():
            csv_file = a_request.FILES['file']
#           payments = PaymentCsvModel.import_from_file(csv_file)
            csv_text = csv_file.read()
            return render(
                a_request,
                'payments/add_payments.html',
                {'table': PaymentsTable(payments),
                 'csv_text': csv_text,
                 'csv_file_type': str(type(csv_file)),
                 }
            )
        else:
            raise ValueError("Form not valid")
    else:
        form = LoadFileForm(a_request)
        return render_to_response(
            'payments/loadpaymentsfile_form.html',
            {'form': form},
            context_instance=RequestContext(a_request),
        )
#       return HttpResponse('<h1>Page was found</h1>')
#       return render_to_response(
#           'payments/loadpaymentsfile_form.html', {'username': username})


def save_payments_list_view(a_request, username):
    if a_request.method != 'POST':
        return HttpResponseNotFound('<h1>No Page Here</h1>')

    payments = a_request.POST.get('csv_text')
    assert False
    return HttpResponseRedirect(
        reverse_lazy('payments', kwargs={'username': username}))
#   if a_request.method == 'POST':
#       pass
#       payments = a_request.session.get('payments')
#       for item in payments.items():
#           p = Payement(corporation=p.corporation,
#               owner=a_request.user,
#               amount=p.amount,
#               title=p.title,
#               due_date=p.due_date,
#               supply_date=p.supply_date,
#               order_date=p.order_date,
#               pay_date=p.pay_date
#           )
#           p.save()


class LoadPaymentsFileView(FormView):
    form_class = LoadFileForm
    template_name = 'payments/loadpaymentsfile_form.html'

    def get_form_kwargs(self):
        kwargs = super(LoadPaymentsFileView, self).get_form_kwargs()
        kwargs['user'] = self.request.user
#         assert False
        return kwargs

    def form_valid(self, form):
        payments = form.get_payments()
        self.request.session['payments'] = payments
        logger.info(self.request.session.get('payments'))
        username = form.user
        self.request.session['username'] = username
        assert False
        return HttpResponseRedirect(
            reverse_lazy('file', kwargs={'username': username,
                                         'payments': payments}))

    # XXX TODO *args, **kwargs might cause problems?
    def post(self, *args, **kwargs):
        form = LoadPaymentsFileForm(request.POST)
        if form.is_valid():
            payments = form.get_payments()
            self.request.session['payments'] = payments
            logger.info(self.request.session.get('payments'))
            username = form.user
            self.request.session['username'] = username
            assert False
        return HttpResponseRedirect(
            reverse_lazy('file', kwargs={'username': username,
                                         'payments': payments}))

    # This is how you decorate class see:
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoadPaymentsFileView, self).dispatch(*args, **kwargs)


class PaymentsFileView(TemplateView):
    #model = Payment
    model = Payment
    template_name = 'payments/file.html'
#     template_name = 'payments/payments.html'
#     template_name = 'payments/file.html'
#     table_class = PaymentsTable

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PaymentsFileView, self).get_context_data(**kwargs)
        context['payments_list'] = self.request.session.get('payments')
#         assert False
        return context

    # This is how you decorate class see:
    # https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PaymentsFileView, self).dispatch(*args, **kwargs)


# login_required
class PaymentCreate(CreateView):

    model = Payment
    form_class = AddPaymentForm
    fields = (
        'corporation',
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


# @login_required
# def add_payments_file(request, username, filename):
#     return HttpResponseRedirect(
#         reverse_lazy('payments'), kwargs={'username': username})


def search(a_request):
    # name__icontains=a_request.POST['search_term'])
    search_term = a_request.GET['search_term'.encode('utf-8')]
    return HttpResponseRedirect(
        reverse_lazy('corporation', kwargs={'corporation': search_term})
        # a_request.POST.get('corporation_name')
    )


def corporation_detail(a_request, corporation):
    obj = get_object_or_404(Corporation, name__icontains=corporation)
    return render(a_request, 'payments/company.html', {'corporation': obj})


# class CorporationView(DetailView):
#     model = Corporation
#     template_name = 'payments/company.html'
#     # context_object_name = 'corporation'
#
#     def get_object(self, *args, **kwargs):
#         return get_object_or_404(Corporation,
#             name__icontains=kwargs['pk'])
