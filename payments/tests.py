from django.test import TestCase
from payments.models import Company

# Create your tests here.
class CompanyTest(TestCase):

    def test_create_company(self):
        self.assertEqual(0, Company.objects.count(), "Expecting 0 objects")
        company = Company.objects.create(
            comapny_name="Hasadna",
            company_url="http://www.hasadna.org.il/",
            email="info@hasadna.org.il",
        )
#         payAvi = Payment.objects.create()
        self.assertEqual(1, Company.objects.count())
