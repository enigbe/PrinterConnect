from unittest import BaseTest

from models.client.cad_model import CADModel
from tests.test_data import cad_model_data


class CADModelTest(BaseTest):
    def test_create_cad_model(self):
        cad_model = CADModel(**cad_model_data)
        self.assertEqual(cad_model, '')

    def test_save_cad_model(self):
        pass

    def test_delete_cad_model(self):
        pass

    def test_update_cad_model(self):
        pass

    def test_compute_cad_model_volume(self):
        pass

    def test_find_cad_model_by_id(self):
        pass

    def test_find_cad_model_by_model_id(self):
        pass

    def test_find_cad_model_by_name(self):
        pass
