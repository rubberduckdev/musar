from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.datetime_safe import datetime
from django.utils.translation import ugettext as _
import json

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else json.JSONEncoder().default(obj)


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

#     def __repr__(self):
#         return json.dumps(self.__dict__, default=dthandler)    
    
    def __unicode__(self):
        return self.name


class PaymentType(object):
    """indication if this is payment to or payment by"""
    IN = 1
    OUT = 2

    choices = (
               (IN, 'In'),
               (OUT, 'Out'),
               )



class Payment(models.Model):
    """ Holds the details of a pass or future payment
        Based on these details the statistics of payments etique are gathered
    """

    corporation = models.ForeignKey(Corporation,
        related_name='corporation_payments',
        verbose_name=_('Corporation ID'),
        # help_text=_('The paying corporation'),
    )
    created_at = models.DateTimeField(auto_now_add=True,
        verbose_name=_('Input date'),
        help_text=_('Created At'),
    )
    owner = models.ForeignKey(User,
        related_name='payments',
        verbose_name=_('Created By'),
        # help_text=_('Who is getting this payment'),
    )
    amount = models.DecimalField(max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name=_('Amount'),
        # help_text=_('How much money should be paid'),
    )
    title = models.CharField(max_length=400,
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
    order_date = models.DateField(default=datetime.now,
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
    
#     def __repr__(self):
#         return json.dumps(self.__dict__, default=dthandler)    

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('add_payments', kwargs={'pk': self.pk})
    
    @classmethod
    def create(cls, corporation, owner, amount, title, due_date, supply_date):
        c = Corporation.objects.get(name=corporation)
        if c==None:
            raise ValueError
        payment = cls(corporation=c, 
            owner=owner, 
            amount=amount, 
            title=title, 
            due_date=due_date, 
            supply_date=supply_date
        )

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")

