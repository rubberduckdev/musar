from datetime import timedelta, date, datetime

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
# from django.utils.datetime_safe import datetime, date
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
import json

MAX_LEGAL_CREDIT_DAYS=45

def dthandler(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    else:
        return json.JSONEncoder().default(obj)


class ShareOption(object):
    """Sharing information policies"""
    NONE = 1
    RESTRICTED = 2
    ALL = 3

    choices = (
        (NONE, 'Share None'),
        (RESTRICTED, 'Share Only With Companies Involved'),
        (ALL, 'Share All'),
    )


class Corporation(models.Model):
    """ Corporation profile """
    cid = models.CharField(
        primary_key=True,
        max_length=200,
        unique=True,
        help_text="Corporation's ID",
    )

    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)


    def __unicode__(self):
        return self.name
    
    @property
    def payments_count(self):
        return self.payment_set.count()
    
    @property
    def total_late_days(self):
        days = 0
        for payment in self.payment_set.all():
            days += payment.lateness_days
        return days
#         return self.payment_set.filter()
    
    @property
    def late_payments_count(self):
        late_payments_set = [payment for payment in self.payment_set.all() \
            if payment.lateness_days > 0]
        return len(late_payments_set)
    
    @property
    def lateness_average(self):
        if self.payments_count == 0:
            return 0
        return self.total_late_days/self.payments_count
    
    @property
    def total_credit_days(self):
        days = 0
        for payment in self.payment_set.all():
            days += payment.credit_days
        return days
        
    @property
    def credit_average(self):
        if self.payments_count == 0:
            return 0
        return self.total_credit_days/self.payments_count
        

class PaymentType(object):
    """indication if this is payment to or payment by"""
    IN = 1
    OUT = 2

    choices = (
        (IN, 'In'),
        (OUT, 'Out'),
    )


def regulation_due_date(supply_date):
    """ Due date might be latter than regulations premits. In such case,
        the latest date regulation allow is returned. 
    """
    max_legal_credit_date = supply_date + timedelta(days=MAX_LEGAL_CREDIT_DAYS)
    return max_legal_credit_date


class Payment(models.Model):
    """ Holds the details of a pass or future payment
        Based on these details the statistics of payments etique are gathered
    """

    corporation = models.ForeignKey(
        Corporation,
#         related_name='corporation_payments',
        verbose_name=_('Corporation ID'),
        # help_text=_('The paying corporation'),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Input date'),
        help_text=_('Created At'),
    )
    owner = models.ForeignKey(
        User,
#         related_name='payments',
        verbose_name=_('Created By'),
        # help_text=_('Who is getting this payment'),
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Amount'),
        # help_text=_('How much money should be paid'),
    )
    title = models.CharField(
        max_length=400,
        verbose_name=_('Description'),
        # help_text=_('Short description of the payment. Who? What for?'),
    )
    due_date = models.DateField(
        verbose_name=_('Due Date'),
        # help_text=_('The date the payment is due'),
    )
    supply_date = models.DateField(
        verbose_name=_('Supply Date'),
        # help_text=_('The date the goods or services where delivared'),
    )
    order_date = models.DateField(
        default=date.today(),
        verbose_name=_('Order Date'),
        # help_text=_('The date the supply was ordered'),
        null=True,
        blank=True,
    )
    pay_date = models.DateField(
        verbose_name=_('Pay Date'),
        # help_text=_('The date the payment was paid'),
        null=True,
        blank=True,
    )

    def __unicode__(self):
        return self.title + " " + self.owner.username + " " + self.corporation.name + " " + str(self.lateness_days) + " " + str(self.supply_date) +  " " + str(self.due_date) + " " + str(self.pay_date) 

    def get_absolute_url(self):
        return reverse('add_payments', kwargs={'pk': self.pk})

    @classmethod
    def create(cls, corporation, owner, amount, title, due_date, supply_date):
        c = Corporation.objects.get(name=corporation)
        if c is None:
            raise ValueError
        payment = cls(
            corporation=c,
            owner=owner,
            amount=amount,
            title=title,
            due_date=due_date,
            supply_date=supply_date
        )

    @property
    def lateness_days(self):
        effective_due_date = min(self.due_date, 
            regulation_due_date(self.supply_date)
        )
        if (self.pay_date == None):
            # ToDo: add test for this if
            return max(0, (date.today() - effective_due_date).days)
        return max((self.pay_date - effective_due_date).days, 0)
    
    @property
    def credit_days(self):
        if (self.pay_date == None):
            # ToDo: add test for this if
            return max(0, (date.today() - self.supply_date).days)
        return max(0, (self.pay_date - self.supply_date).days)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        

class UserProfile(models.Model):  
    user = models.OneToOneField(User) 
    neardue_days = models.DecimalField(default=6, decimal_places=0, max_digits=2) 

    def __str__(self):  
          return "%s's profile" % self.user  

    def create_user_profile(sender, instance, created, **kwargs):  
        if created:  
           profile, created = UserProfile.objects.get_or_create(user=instance)
    
    @property
    def overdue_payments(self):
        late_payments = [
            payment for payment in self.user.payment_set.all() 
                if payment.lateness_days > 0 
        ]
        return late_payments
         
    @property
    def neardue_payments(self):
        neardue_payments = []
        for payment in self.user.payment_set.all():
            days_till_pay = (date.today() - payment.due_date).days
            print "days", days_till_pay
            if days_till_pay > 0 and days_till_pay <= 6:
                print "APPEND", payment.due_date
                neardue_payments.append(payment)
            
#         neardue_payments = Payment.objects.filter(due_date__range=(startdate, enddate))
#         neardue_payments = Payment.objects.filter(due_date__range=(startdate, enddate))
#                                                   ,
#             due_date__range=[startdate, enddate])
 
        return neardue_payments

    @property       
    def payments_count_by_corporation(self, corporation):
        payments_list = [payment for payment in self.user.payment_set.all() \
            if payment.corporation == corporation]
        return len(payments_list)
           
    @property
    def payments_count(self):
        return self.user.payment_set.count()
    
    @property
    def total_late_days(self):
        days = 0
        for payment in self.user.payment_set.all():
            days += payment.lateness_days
        return days
    
    @property
    def late_payments_count(self):
        late_payments = [payment for payment in self.user.payment_set.all() \
            if payment.lateness_days > 0]
        return len(late_payments)
    
    @property
    def lateness_average(self):
        if self.payments_count > 0:
            return self.total_late_days/self.payments_count
        return 0
    
    @property
    def total_credit_days(self):
        days = 0
        for payment in self.user.payment_set.all():
            days += payment.credit_days
        return days
        
    @property
    def credit_average(self):
        if self.payments_count > 0:
            return self.total_credit_days/self.payments_count
        return 0

    post_save.connect(create_user_profile, sender=User) 
        
        

