from adaptor.model import CsvModel
from adaptor.fields import DateField, DjangoModelField, CharField, DecimalField
from payments.models import Payment, Corporation
from django.contrib.auth.models import User
import json

dthandler = lambda obj: obj.isoformat() if isinstance(obj, datetime) else json.JSONEncoder().default(obj)

#https://github.com/anthony-tresontani/django-adaptors/blob/master/docs/index.rst
class PaymentCsvModel(CsvModel):
    corporation =  DjangoModelField(Corporation)
    amount = DecimalField()
    title = CharField()
    due_date = DateField(format="%d-%m-%Y")
    supply_date = DateField(format="%d-%m-%Y")
    order_date = DateField(format="%d-%m-%Y")
    pay_date = DateField(format="%d-%m-%Y")

    
    def __repr__(self):
        return json.dumps(self.__dict__, default=dthandler)    
 
    class Meta:
        delimiter = ","