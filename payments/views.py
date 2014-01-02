from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from payments.models import Company

# Create your views here.

def index(request):
    return render(request, 'payments/index.html')


def register(request):
    return render(request, 'payments/register.html')

@login_required
def after_login(request):
    username = request.user.username
    return HttpResponseRedirect(reverse_lazy('home', kwargs={'username': username}))


#@login_required
#def home(request, username):
#    return render(request, 'payments/home.html', {'username': username})


class HomeView(ListView):

    template_name = 'payments/home.html'
    context_object_name = 'my_companies'
    Model = Company
 
    def get_payments(company_name):
        return Company.objects.filter(company__name=company_name)
 
    def get_queryset(self):
        return self.request.user.companies.all()

    """This is how you decorate class see:
       https://docs.djangoproject.com/en/1.5/topics/class-based-views/intro/"""
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HomeView, self).dispatch(*args, **kwargs)
    
 
def statistics(request, username):
    return render(request, 'payments/statistics.html', {'username': username})


def settings(request, username):
    return render(request, 'payments/settings.html', {'username': username})


def search(request):
    return render(request, 'payments/search.html')

