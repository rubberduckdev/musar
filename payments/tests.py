from django.test import TestCase
from django.contrib.auth.models import User#, UserProfile
from datetime import timedelta
from django.utils.datetime_safe import datetime, date
# from django.utils.datetime_safe import datetime as  django_datetime
from payments.models import (
    Corporation, Payment, regulation_due_date
)


# Create your tests here.

#class CompanyTest(TestCase):
#
#    def test_create_company(self):
#        Company.objects.create(
#            cid='123',
#            name="Hasadna",
#            url="http://www.hasadna.org.il/",
#            email="info@hasadna.org.il",
#
#        )
#
#        self.assertEqual(1, Company.objects.count())
#
#        Company.objects.create(
#            cid='abc',
#            name="Avi",
#            url="http://www.avi.co.il/",
#            email="info@avi.co.il",
#        )
#        self.assertEqual(
#            2, Company.objects.count()
#        )
#
#        # Test retrieve companies by name
#        self.assertEqual(1, Company.objects.filter(name='Hasadna').count())
#        self.assertEqual(1, Company.objects.filter(name='Avi').count())
#        self.assertEqual(0, Company.objects.filter(name='Moshe').count())
#        # TODO: how do I retrieve the preferences for company2
#
#
#class PaymentTest(TestCase):
#
#    def setUp(self):
#        self.company1 = Company.objects.create(
#            cid='sc1',
#            name="FSF",
#            url="http://www.fsf.org/",
#            email="info@fsf.org",
#        )
#        self.company2 = Company.objects.create(
#            cid='sc2',
#            name="Yossi",
#            url="http://www.yossi.co.il/",
#            email="info@yossi.co.il",
#        )
#
#    def test_create_payment(self):
#        Payment.objects.create(
#            buyer=self.company1,
#            seller=self.company2,
#            dueDate=datetime.now(),
#            orderdate=datetime.now(),
#            input_user=self.company1,
#        )
#        self.assertEqual(1, Payment.objects.count())
#
#    #       Test in and out payments counts before and after creating a
#    #       payment
#    def test_company_payements_associations(self):
#
#        self.assertEqual(
#            0, self.company1.out_payments.count(),
#        )
#        self.assertEqual(
#            0, self.company2.out_payments.count(),
#        )
#        self.assertEqual(
#            0, self.company1.in_payments.count(),
#        )
#        self.assertEqual(
#            0, self.company2.in_payments.count(),
#        )
#
#        self.assertEqual(0, Payment.objects.count())
#
#        Payment.objects.create(
#            buyer=self.company1,
#            seller=self.company2,
#            dueDate=datetime.now(),
#            orderdate=datetime.now(),
#            input_user=self.company1,
#        )
#        self.assertEqual(
#            1, Payment.objects.count())
#
#        self.assertEqual(
#            1, self.company1.out_payments.count(),
#        )
#
#        self.assertEqual(
#            0, self.company2.out_payments.count(),
#        )
#
#        self.assertEqual(
#            0, self.company1.in_payments.count(),
#        )
#
#        self.assertEqual(
#            1, self.company2.in_payments.count(),
#        )
#
#

class CorporationTests(TestCase):
    
    def setUp(self):
        self.user_c1 = User.objects.create(username='user1')
        self.user_c2 = User.objects.create(username='user2')
        self.c1 = Corporation.objects.create(
            cid='87654321', name='CorporationTests1'
        )

        self.c2 = Corporation.objects.create(
            cid='12345678', name='CorporationTests2'
        )
        
        self.late_days_1 = 84

        supply_date_1 = date(2014, 12, 05)
        due_date_1 = regulation_due_date(supply_date_1)
        pay_date_1 = due_date_1 + timedelta(days=self.late_days_1)
        
        self.credit_days_1 = (pay_date_1 - supply_date_1).days

        self.p1 = Payment.objects.create(
            corporation=self.c1,
            owner=self.user_c1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date_1,
            supply_date=supply_date_1,
            #order_date=d1,
            pay_date=pay_date_1
        )
        
        self.late_days_2 = 10

        """ legal due date
        """
        supply_date_2 = date(2014, 05, 31)
        due_date_2 = regulation_due_date(supply_date_2)
        pay_date_2 = due_date_2 + timedelta(days=self.late_days_2)
        
        self.credit_days_2 = (pay_date_2 - supply_date_2).days

        self.p2 = Payment.objects.create(
            corporation=self.c1,
            owner=self.user_c2,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date_2,
            supply_date=supply_date_2,
            #order_date=d1,
            pay_date=pay_date_2
        )
        
        self.late_days_3 = 10
        
        supply_date_3 = date(2014, 02, 15)
        due_date_3 = regulation_due_date(supply_date_3)
        pay_date_3 = due_date_3 + timedelta(days=self.late_days_3)
        
        self.credit_days_3 = (pay_date_3 - supply_date_3).days

        
        self.p3 = Payment.objects.create(
            corporation=self.c2,
            owner=self.user_c2,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date_3,
            supply_date=supply_date_3,
            #order_date=d1,
            pay_date=pay_date_3
        )
        
  
    def tearDown(self):
        self.c1.delete()
        self.c2.delete()
        self.user_c1.delete()
        self.user_c2.delete()
        self.p1.delete()
        self.p2.delete()
        self.p3.delete()
  
    def test_get_total_late_days(self):

        """ test for corporation c1
        """
        self.assertEqual(self.c1.total_late_days, 
            self.late_days_1 
            + self.late_days_2
        )
        
        """ test for corporation c2
        """
        self.assertEqual(self.c2.total_late_days, self.late_days_3) 
    
    def test_payments_count(self):
        self.assertEqual(self.c1.payments_count, 2)
        self.assertEqual(self.c2.payments_count, 1)
    
    def test_late_payments_count(self):
        
        """ add on-time payments 
        """
        supply_date = date(2014, 10, 15)
        due_date = regulation_due_date(supply_date)
        
        self.p4 = Payment.objects.create(
            corporation=self.c1,
            owner=self.user_c2,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=due_date
        )
        
        self.p5 = Payment.objects.create(
            corporation=self.c2,
            owner=self.user_c2,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=due_date
        )
        self.assertEqual(self.c1.late_payments_count, 2)
        self.assertEqual(self.c2.late_payments_count, 1)
        self.assertEqual(Payment.objects.count(), 5)
        
    def test_lateness_avarege(self):
        self.assertEqual(self.c1.lateness_average, (self.late_days_1 +
            self.late_days_2)/2
        )
        self.assertEqual(self.c2.lateness_average, self.late_days_3)
        
    def test_total_credit_days(self):
        self.assertEqual(self.c1.total_credit_days, self.credit_days_1 + self.credit_days_2)
        self.assertEqual(self.c2.total_credit_days, self.credit_days_3)

    def test_credit_avarege(self):
        self.assertEqual(self.c1.credit_average, (self.credit_days_1 +
            self.credit_days_2)/2
        )
        self.assertEqual(self.c2.credit_average, self.credit_days_3)
        

class PaymentsTests(TestCase):
    
    def setUp(self):
        self.user_1 = User.objects.create(username='user1')
        self.corporation_1 = Corporation.objects.create(
            cid="PaymentsTests"
        )


        """
supply: time of goods delivery-
due: agreed time of payment
pay: actual time of payment
credit:

Le diagram
----------

```
        |-------|---------|
    supply    due       pay

        |-----------------|
          credit_days

                |---------|
                 late_days
```

        credit_days = max(pay_date - supply_date, 0)
            # credit_days >= 0

        late_days = max(
            pay_date - min(due_date, max_legal_due_date), 0)
            # late_days >= 0

        pay_date = min(due_date, max_legal_due_date) + late_days
        = supply_date + credit_days

        max_legal_due_date = supply_date + 45

        credit_days - late_days = due_date - supply_date

        due_date = supply_date
                 + timedelta(days=credit_days - late_days)
        """

        #http://stackoverflow.com/questions/151199/how-do-i-calculate-number-of-days-betwen-two-dates-using-python
        #http://docs.python.org/2/library/datetime.html

    def tearDown(self):
        self.corporation_1.delete()
        self.user_1.delete()

    def test_lateness_when_late(self):
        """
Le diagram
----------

```
        |-------|---------|
    supply    due       pay

        |-----------------|
          credit_days

                |---------|
                 late_days
```
        """

        late_days = 84

        supply_date = date(2008, 8, 18)
        due_date = regulation_due_date(supply_date) - timedelta(days=3)
        pay_date = due_date + timedelta(days=late_days)

        p1 = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(p1.lateness_days, late_days)

    def test_lateness_when_payment_exactly_on_due_time(self):
        """
Le diagram
----------

```
        |-----------------|
    supply            due/pay       

        |-----------------|
          credit_days

                |---------|
                 late_days
```
        """
        credit_days = 30
        late_days = 0

        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=credit_days-late_days)
        pay_date = due_date + timedelta(days=late_days)

        p1 = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(p1.lateness_days, late_days)
    
    def test_lateness_when_payment_before_due_time(self):
        """
Le diagram
----------

```
        |-------|---------|
    supply    pay       due

        |-------|
       credit_days
-->
time
```
        """

        credit_days = 20


        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=30)
        pay_date = supply_date + timedelta(days=credit_days)

        our_payment = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(our_payment.lateness_days, 0)

    def test_lateness_when_payment_before_supply(self):
        """
Le diagram
----------

```
        |-------|---------|
      pay    supply      due
-->
time
```
        """

        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=30)
        pay_date = supply_date - timedelta(days=20)

        our_payment = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(our_payment.lateness_days, 0)

    def test_lateness_when_due_date_is_illegal(self):
        """
Le diagram
----------

```
        |-----------|----------|-----|

      ------   ------------   ---   ---
     |supply| |   45 days  | |due| |pay|
      ------  |since supply|  ---   ---
               ------------

        |----------------------------|
                    ------
                   |credit|
                    ------
    -->
    time
```
        """

        legal_max_days = 45

        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=legal_max_days + 15)
        pay_date = due_date + timedelta(days=10)
        late_days = 25

        our_payment = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(our_payment.lateness_days, late_days)

    def test_credit(self):
        """
Le diagram
----------

```
        |-----------------|
    supply               pay

        |-----------------|
           credit_days
-->
time
```
        """

        legal_max_days = 45

        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=legal_max_days + 15)
        pay_date = due_date + timedelta(days=10)
        late_days = 0
        credit_days = (pay_date - supply_date).days

        our_payment = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )
        print our_payment.credit_days
        self.assertEqual(our_payment.credit_days, credit_days)
    
    def test_credit_when_payment_before_supply_time(self):

        """
Le diagram

```
        |-----------------|
       pay             supply

         no credit
>
time
```
        """
        credit_days = 0


        supply_date = date(2008, 8, 18)
        due_date = supply_date + timedelta(days=30)
        pay_date = supply_date - timedelta(days=10)

        our_payment = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            pay_date=pay_date
        )

        self.assertEqual(our_payment.credit_days, credit_days)

    def test_credit_with_no_pay_date(self):
        
        credit_days = 30
        
        supply_date = date.today() - timedelta(days=credit_days)
        due_date = supply_date + timedelta(days=credit_days)

        p1 = Payment.objects.create(
            corporation=self.corporation_1,
            owner=self.user_1,
            #amount=csv_model.amount,
            #title=csv_model.title,
            due_date=due_date,
            supply_date=supply_date,
            #order_date=d1,
            #pay_date=pay_date
        )

        self.assertEqual(p1.credit_days, credit_days)
    
