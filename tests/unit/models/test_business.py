from unittest import TestCase
from models.business.business import BusinessModel
from tests.test_data import business


class BusinessModelTest(TestCase):
    def test_create_business_model(self):
        business_instance = BusinessModel(**business)
        created_business_account = f'<Business => @{business["username"]}: {business["business_name"]}>'
        self.assertEqual(business_instance.__repr__(), created_business_account)
