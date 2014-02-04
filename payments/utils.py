from datetime import date

from payments.models import Payment

def lateness_days(payment):
    pass
    return (payment.due_date - payment.pay_date).days

def credit_days(payment):
    pass
    return (payment.supply_date - payment.pay_date).days
