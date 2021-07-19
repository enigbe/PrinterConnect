from tests.base_test import BaseTest
from tests.test_data import business
from models.business.business import BusinessModel


class BusinessModelTest(BaseTest):
    def test_find_business_by_username(self):
        with self.app_context():
            business_instance = BusinessModel(**business)
            self.assertIsNone(BusinessModel.find_business_by_username(business['username']))
            business_instance.save_business_to_db()
            self.assertIsNotNone(BusinessModel.find_business_by_username(business['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')

    def test_save_business_to_db(self):
        with self.app_context():
            business_instance = BusinessModel(**business)
            self.assertIsNone(BusinessModel.find_business_by_username(business['username']))
            business_instance.save_business_to_db()
            self.assertIsNotNone(BusinessModel.find_business_by_username(business['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')

    def test_delete_business_from_db(self):
        with self.app_context():
            business_instance = BusinessModel(**business)
            self.assertIsNone(BusinessModel.find_business_by_username(business['username']))
            business_instance.save_business_to_db()
            self.assertIsNotNone(BusinessModel.find_business_by_username(business['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')
            business_instance.delete_business_from_db()
            self.assertIsNone(BusinessModel.find_business_by_username(business['username']))
