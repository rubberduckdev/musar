from django.forms.models import ModelForm
from payments.models import Payment, Corporation
import floppyforms as forms


class AddPaymentForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if kwargs.get('instance'):
            kwargs.setdefault('initial', {})['owner'] = self.user
        super(AddPaymentForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Payment
        fields = ('corporation',
            'title',
            'amount',
            'due_date',
            'supply_date',
            'pay_date'
        )
        widgets = {
            'title': forms.TextInput(),
            'due_date': forms.DateInput(),
            'supply_date': forms.DateInput(),
            'pay_date': forms.DateInput(),
        }


class select_corporation_form():
    class Meta:
        model = Corporation
        fields = ('corporation',)
        widgets = {
            'corporation': forms.TypedChoiceField(),
        }

