from tests.base_test import BaseTest
from tests.test_data import business_data
from models.business.business import BusinessModel


class BusinessModelTest(BaseTest):
    def test_find_business_by_username(self):
        with self.app_context():
            business_instance = BusinessModel(**business_data)
            self.assertIsNone(BusinessModel.find_user_by_username(business_data['username']))
            business_instance.save_user_to_db()
            self.assertIsNotNone(BusinessModel.find_user_by_username(business_data['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')

    def test_save_business_to_db(self):
        with self.app_context():
            business_instance = BusinessModel(**business_data)
            self.assertIsNone(BusinessModel.find_user_by_username(business_data['username']))
            business_instance.save_user_to_db()
            self.assertIsNotNone(BusinessModel.find_user_by_username(business_data['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')

    def test_delete_business_from_db(self):
        with self.app_context():
            business_instance = BusinessModel(**business_data)
            self.assertIsNone(BusinessModel.find_user_by_username(business_data['username']))
            business_instance.save_user_to_db()
            self.assertIsNotNone(BusinessModel.find_user_by_username(business_data['username']))
            self.assertEqual(business_instance.__class__.__name__, 'BusinessModel')
            business_instance.delete_user_from_db()
            self.assertIsNone(BusinessModel.find_user_by_username(business_data['username']))
