from django.db import models
from django.utils.datetime_safe import datetime
from django.contrib.auth.models import User


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


class Company(models.Model):
    """ Company profile """
    cid = models.CharField(
        primary_key=True,
        max_length=200,
        unique=True,
        help_text="Company's ID",
    )

    users = models.ManyToManyField(
        User,
        related_name='companies',
        help_text='list of users with permission to edit the company profile',
    )

    name = models.CharField(max_length=200, unique=True)
    url = models.URLField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    shared_with = models.IntegerField(
        choices=ShareOption.choices,
        default=ShareOption.NONE,
        help_text='company\'s sharing data policy',
    )

    def __unicode__(self):
        return self.name


# FIXME: check why http://localhost:8000/admin/payments/partner/ fails
class Partner(models.Model):
    """ Company profile """
    company = models.ForeignKey(Company)

#     users = models.ManyToManyField(User, related_name='partners')

    name = models.CharField(max_length=200, unique=True)

    url = models.URLField(null=True, blank=True)

    email = models.EmailField(null=True, blank=True)

    shared_with = models.IntegerField(
        choices=ShareOption.choices,
        default=ShareOption.NONE,
        help_text='Stores the company\'s prefrences for sharing data',
    )

    def __unicode__(self):
        return self.name


class PaymentDirection(object):
    """indication if this is payment to or payment by"""
    IN = 1
    OUT = 2

    choices = (
        (IN, 'In'),
        (OUT, 'Out'),
    )


class Payment(models.Model):
    """Represent private money transaction"""

    partner = models.ForeignKey(
        Partner,
        related_name='partner_payments',
        help_text='The other side of the transaction',
    )

    owner = models.ForeignKey(
        Partner,
        related_name='my_payments',
        help_text='The company associated with this transaction',
    )

    created_at = models.DateTimeField(auto_now_add=True)

    created_by = models.ForeignKey(User)

    direction = models.IntegerField(choices=PaymentDirection.choices)

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    title = models.CharField(max_length=400)

    due_date = models.DateField()

    order_date = models.DateField(default=datetime.now, null=True, blank=True)

    # Date at which payment was finally paid
    payment_date = models.DateField(null=True, blank=True)

    shared_with = models.IntegerField(
        choices=ShareOption.choices,
        default=ShareOption.NONE,
    )

    def __unicode__(self):
        return self.title
