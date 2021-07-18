from tests.base_test import BaseTest
from models.client.cad_model import CADModel
from models.client.client import ClientModel
from schema.client.cad_model import CADSpecificationSchema
from tests.test_data import cad_model_data, client


class CADModelTest(BaseTest):
    def test_create_cad_model(self):
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_id(sample_client.id))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_id(sample_client.id))
            cad_model = CADModel(client_id=sample_client.id, **cad_model_data)
            schema = CADSpecificationSchema()
            cad_model_dict = schema.dump(cad_model)
            self.assertEqual(cad_model_dict['cad_model_width'], 12.5)
            self.assertEqual(cad_model_dict['cad_model_length'], 12.5)

    def test_save_cad_model(self):
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_id(sample_client.id))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_id(sample_client.id))
            # Create CADModel and save to DB
            cad_model = CADModel(client_id=sample_client.id, **cad_model_data)
            self.assertIsNone(CADModel.find_cad_model_by_id(1))
            cad_model.save_cad_model_to_db()
            self.assertIsNotNone(CADModel.find_cad_model_by_id(1))

    def test_delete_cad_model(self):
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_id(sample_client.id))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_id(sample_client.id))
            # Create CADModel and save to DB
            cad_model = CADModel(client_id=sample_client.id, **cad_model_data)
            self.assertIsNone(CADModel.find_cad_model_by_id(1))
            cad_model.save_cad_model_to_db()
            self.assertIsNotNone(CADModel.find_cad_model_by_id(1))
            # Delete CADModel from DB
            cad_model.delete_cad_model_from_db()
            self.assertIsNone(CADModel.find_cad_model_by_id(1))

    def test_update_cad_model(self):
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_id(sample_client.id))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_id(sample_client.id))
            # Create CADModel and save to DB
            cad_model = CADModel(client_id=sample_client.id, **cad_model_data)
            self.assertIsNone(CADModel.find_cad_model_by_id(1))
            cad_model.save_cad_model_to_db()
            self.assertIsNotNone(CADModel.find_cad_model_by_id(1))
            # Update CADModel property
            cad_model.cad_model_length = 50
            cad_model.update_cad_model_in_db()
            self.assertEqual(cad_model.cad_model_length, 50)

    def test_compute_cad_model_volume(self):
        with self.app_context():
            # Create and save a client to DB
            sample_client = ClientModel(**client)
            self.assertIsNone(ClientModel.find_client_by_id(sample_client.id))
            sample_client.save_client_to_db()
            self.assertIsNotNone(ClientModel.find_client_by_id(sample_client.id))
            # Create CADModel and save to DB
            cad_model = CADModel(client_id=sample_client.id, **cad_model_data)
            self.assertIsNone(CADModel.find_cad_model_by_id(1))
            cad_model.save_cad_model_to_db()
            self.assertIsNotNone(CADModel.find_cad_model_by_id(1))
            # Compute volume
            self.assertEqual(cad_model.cad_model_volume, 1953.125)
