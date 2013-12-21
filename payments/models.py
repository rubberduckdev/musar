from django.db import models
from django.utils.datetime_safe import datetime


class Company(models.Model):
    """ Company profile """
    cid = models.CharField(
        primary_key=True,
        max_length=200, unique=True
    )
    name = models.CharField(max_length=200, unique=True)
    url = models.URLField()
    email = models.EmailField()

    def __unicode__(self):
        return self.name


class Payment(models.Model):
    """ Represent money transaction """
    buyer = models.ForeignKey(Company, related_name='out_payments', null=True)
    seller = models.ForeignKey(Company, related_name='in_payments', null=True)
#   TODO: See https://piazza.com/class/hnyk6a1pnyd6dd
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dueDate = models.DateField()
    orderdate = models.DateField(default=datetime.now(), null=True)
    input_date = models.DateTimeField(auto_now_add=True)
    input_user = models.ForeignKey(Company)
    restrict_share = models.BooleanField(default=False)
    verfied = models.BooleanField(default=False)
#   TODO: verified_by


class Preferences(models.Model):
    """ Stores the company's prefrences for sharing data and for alerts """
    SHARE_ALL = 'SA'
    SHARE_NONE = 'SN'
    SHARE_RESTRICTED = 'SR'
    SHARING_POLICY_SEQ = (
                    (SHARE_ALL, 'Share All'),
                    (SHARE_NONE, 'Share None'),
                    (SHARE_RESTRICTED, 'Share Only With Companies Involved'),
    )
    sharing_policy = models.CharField(
        max_length=2,
        choices=SHARING_POLICY_SEQ,
        default=SHARE_NONE,
    )
    alerts = models.CharField(max_length=200)
    company = models.OneToOneField(
        Company,
        related_name='company',
    )
