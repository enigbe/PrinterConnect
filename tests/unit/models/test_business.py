from unittest import TestCase
from models.business.business import BusinessModel
from tests.test_data import business_data


class BusinessModelTest(TestCase):
    def test_create_business_model(self):
        business_instance = BusinessModel(**business_data)
        created_business_account = f'<Business => @{business_data["username"]}: {business_data["business_name"]} - (' \
                                   f'{business_data["email"]})>'
        self.assertEqual(business_instance.__repr__(), created_business_account)
