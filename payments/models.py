from django.db import models
from django.utils.datetime_safe import datetime


class Company(models.Model):
    """ Company profile """
    id = models.CharField(primary_key=True, max_length=200, unique=True)
    comapny_name = models.CharField(max_length=200, unique=True)
    company_url = models.URLField()
    email = models.EmailField()
    payements = models.ManyToOneRel()

    def __unicode__(self):
        return self.comapny_name

# TODO: consider wrapping SHARE_XXX in class for better namespacing
SHARE_ALL = 'SA'
SHARE_NONE = 'SN'
SHARE_RESTRICTED = 'SR'

SHARING_POLICY_SEQ = (
    (SHARE_ALL, 'Share All'),
    (SHARE_NONE, 'Share None'),
    (SHARE_RESTRICTED, 'Share Only With Companies Involved'),
)


class Payment(models.Model):
    """ Represent money transaction """
    buyer = models.ForeignKey(Company, related_name='buyer', blank=True)
    seller = models.ForeignKey(Company, related_name='seller', blank=True)
#   TODO: See https://piazza.com/class/hnyk6a1pnyd6dd
#   amount = MoneyField(max_digits=10, decimal_places=2, default_currency='USD')
    dueDate = models.DateField()
    orderdate = models.DateField(default=datetime.now(), blank=True)
    input_date = models.DateTimeField(auto_now_add=True)
    input_user = models.ForeignKey(Company)
    restrict_share = models.BooleanField(default=False)
    verfied = models.BooleanField(default=False)
#   TODO: verified_by


class Preferences(models.Model):
    """ Stores the company's prefrences for sharing data and for alerts"""
    company = models.ForeignKey(Company)
    sharing_policy = models.CharField(
        max_length=2,
        choices=SHARING_POLICY_SEQ,
        default=SHARE_RESTRICTED,
    )
    #alerts
'''


Preferences
Company.id 
SharingPolicy.id
Alerts

SharingPolicy
id (auto-int)
TBD

Alert
name
is_on (boolean)
'''