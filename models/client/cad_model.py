from datetime import datetime
from data_base import db


class CADModel(db.Model):
    """Model for CAD models uploaded by clients"""
    __tablename__ = 'cad_models'

    id = db.Column(db.Integer, primary_key=True)
    cad_model_id = db.Column(db.String(100), nullable=False)
    cad_model_name = db.Column(db.String(100), nullable=False)
    cad_model_height = db.Column(db.Float(precision=2), nullable=False)  # model height in millimeters
    cad_model_width = db.Column(db.Float(precision=2), nullable=False)  # model width in millimeters
    cad_model_length = db.Column(db.Float(precision=2), nullable=False)  # model length in millimeters
    cad_model_material = db.Column(db.String(100), nullable=False)
    cad_model_mesh_percent = db.Column(db.Integer, nullable=False)  # print mesh percentage in %
    cad_model_visibility = db.Column(db.Boolean, default=False)
    cad_model_creation_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    client = db.relationship('ClientModel')

    @classmethod
    def find_cad_model_by_id(cls, _id: int) -> "CADModel":
        """Searches and returns a CAD model by its ID, if it exists"""
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_cad_model_by_name(cls, cad_model_name: str) -> "CADModel":
        """Searches for and returns a CAD model bu its name, if it exists"""
        return cls.query.filter_by(cad_model_name=cad_model_name).first()

    @classmethod
    def find_cad_model_by_model_id(cls, cad_model_id: str) -> "CADModel":
        """Searches for and returns a CAD model bu its name, if it exists"""
        return cls.query.filter_by(cad_model_id=cad_model_id).first()

    def save_cad_model_to_db(self) -> None:
        """Save the CAD model to the database"""
        db.session.add(self)
        db.session.commit()

    def update_cad_model_in_db(self) -> None:
        """Update the CAD model"""
        db.session.commit()

    def delete_cad_model_from_db(self) -> None:
        """Delete CAD model from database"""
        db.session.delete(self)
        db.session.commit()

    def rollback_cad_model_changes(self):
        """Roll back changes in the current session"""
        db.session.rollback()

    @property
    def cad_model_volume(self):
        """Computes and returns the volume of the CAD model in cubic millimeters"""
        return self.cad_model_height * self.cad_model_length * self.cad_model_width
