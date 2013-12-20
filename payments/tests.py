from django.test import TestCase
from datetime import datetime
from payments.models import (
    Company, Payment, Preferences,
)


# Create your tests here.

class CompanyCreateTest(TestCase):
    def test_create_company(self):
        company1 = Company.objects.create(
            cid = '123',
            name="Hasadna",
            url="http://www.hasadna.org.il/",
            email="info@hasadna.org.il",

        )
        self.assertEqual(1, Company.objects.count())
        company2 = Company.objects.create(
            cid = 'abc',
            name="Avi",
            url="http://www.avi.co.il/",
            email="info@avi.co.il",
        )
        self.assertEqual(2, Company.objects.count())

        self.assertEqual(
            0, company1.out_payments.count(),
        )
        self.assertEqual(
            0, company2.out_payments.count(),
        )
        self.assertEqual(
            0, company1.in_payments.count(),
        )
        self.assertEqual(
            0, company2.in_payments.count(),
        )

        self.assertEqual(0, Payment.objects.count())

        payAvi = Payment.objects.create(
            buyer=company1,
            seller=company2,
            dueDate=datetime.now(),
            orderdate=datetime.now(),
            input_user=company1,
            restrict_share=False,
        )
        self.assertEqual(
            1, Payment.objects.count())

        self.assertEqual(
            1, company1.out_payments.count(),
        )

        self.assertEqual(
            0, company2.out_payments.count(),
        )

        self.assertEqual(
            0, company1.in_payments.count(),
        )

        self.assertEqual(
            1, company2.in_payments.count(),
        )


class PaymentTest(TestCase):
    def setUp(self):
        self.setuped_company_1 = Company.objects.create(
            cid='sc1',
            name="FSF",
            url="http://www.fsf.org/",
            email="info@fsf.org",
        )
        self.setuped_company_2 = Company.objects.create(
            cid='sc2',
            name="Yossi",
            url="http://www.yossi.co.il/",
            email="info@yossi.co.il",
        )

    def test_payment(self):
        '''
        self.assertEqual()
        '''
