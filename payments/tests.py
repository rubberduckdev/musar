from django.test import TestCase
from datetime import datetime
from payments.models import (
    Company, Payment, Settings,
)


# Create your tests here.

class CompanyTest(TestCase):

    def test_create_company(self):
        Company.objects.create(
            cid='123',
            name="Hasadna",
            url="http://www.hasadna.org.il/",
            email="info@hasadna.org.il",

        )

        self.assertEqual(1, Company.objects.count())

        Company.objects.create(
            cid='abc',
            name="Avi",
            url="http://www.avi.co.il/",
            email="info@avi.co.il",
        )
        self.assertEqual(
            2, Company.objects.count()
        )

        """ Test retrive companies by name"""
        self.assertEqual(
            1,
            Company.objects.filter(name='Hasadna').count())
        self.assertEqual(
            1,
            Company.objects.filter(name='Avi').count())
        self.assertEqual(
             0,
             Company.objects.filter(name='Moshe').count())
        # TODO: how do I retrieve the preferences for company2


class PaymentTest(TestCase):

    def setUp(self):
        self.company1 = Company.objects.create(
            cid='sc1',
            name="FSF",
            url="http://www.fsf.org/",
            email="info@fsf.org",
        )
        self.company2 = Company.objects.create(
            cid='sc2',
            name="Yossi",
            url="http://www.yossi.co.il/",
            email="info@yossi.co.il",
        )

    def test_create_payment(self):
        Payment.objects.create(
            buyer=self.company1,
            seller=self.company2,
            dueDate=datetime.now(),
            orderdate=datetime.now(),
            input_user=self.company1,
        )
        self.assertEqual(
            1, Payment.objects.count())

    """
            Test in and out payments counts before and after creating a
            payment
    """
    def test_company_payements_associations(self):

        self.assertEqual(
            0, self.company1.out_payments.count(),
        )
        self.assertEqual(
            0, self.company2.out_payments.count(),
        )
        self.assertEqual(
            0, self.company1.in_payments.count(),
        )
        self.assertEqual(
            0, self.company2.in_payments.count(),
        )

        self.assertEqual(0, Payment.objects.count())

        Payment.objects.create(
            buyer=self.company1,
            seller=self.company2,
            dueDate=datetime.now(),
            orderdate=datetime.now(),
            input_user=self.company1,
        )
        self.assertEqual(
            1, Payment.objects.count())

        self.assertEqual(
            1, self.company1.out_payments.count(),
        )

        self.assertEqual(
            0, self.company2.out_payments.count(),
        )

        self.assertEqual(
            0, self.company1.in_payments.count(),
        )

        self.assertEqual(
            1, self.company2.in_payments.count(),
        )
