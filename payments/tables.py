from django_tables2 import tables, columns
from payments.models import Payment


class PaymentsTable(tables.Table):
    class Meta:
        model = Payment
        exclude = ('owner', 'created_at')
        order_date = columns.DateColumn()
        supply_date = columns.DateColumn()
        due_date = columns.DateColumn()
        pay_date = columns.DateColumn()
        sequence = (
            'id',
            'corporation',
            'title',
            'amount',
            'order_date',
            'supply_date',
            'due_date',
            'pay_date',
        )
        attrs = {"class": "table"}


class PaymentsPartialTable(tables.Table):

    action = columns.TemplateColumn(
        accessor='corporation.email',
        verbose_name='Send Reminder',
        template_name='payments/send_reminder.html',
        orderable=False)

    last_reminder = columns.Column(verbose_name='Last Reminder',)

    class Meta:
        model = Payment
        due_date = columns.DateColumn()
        exclude = (
            'owner',
            'created_at',
            'id',
            'order_date',
            'supply_date',
            'pay_date'
        )
        sequence = (
            'corporation',
            'title',
            'amount',
            'due_date',
            'last_reminder',
            'action',
        )
        attrs = {"class": "table"}
