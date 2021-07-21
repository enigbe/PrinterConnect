from tests.base_test import BaseTest
from tests.test_data import business_data


class BusinessEmailSignUpTest(BaseTest):
    def test_business_signup_with_email_password(self):
        with self.app() as test_client, self.app_context():
            resp = test_client.post('/business/email/signup', json=business_data)
            self.assertEqual(resp.status, 201)
