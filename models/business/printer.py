import enum
from data_base import db


class Material(str, enum.Enum):
    PLA = 'PLA'
    ABS = 'ABS'
    ASA = 'ASA'
    HIPS = 'HIPS'
    PETG = 'PETG'
    NYLON = 'NYLON'
    CFF = 'CFF'
    PCB = 'PCB'
    PVA = 'PVA'


class FileType(str, enum.Enum):
    STL = 'STL'
    OBJ = 'OBJ'
    AMF = 'AMF'
    _3MF = '_3MF'
    PLY = 'PLY'
    STEP = 'STEP'
    IGES = 'IGES'


class PrinterModel(db.Model):
    __tablename__ = 'printers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True)
    model = db.Column(db.String(100), nullable=True)
    base_width = db.Column(db.Float(precision=2), nullable=False)
    base_length = db.Column(db.Float(precision=2), nullable=False)
    height = db.Column(db.Float(precision=2), nullable=False)
    nozzle_diameter = db.Column(db.Float(precision=2), nullable=False)
    file_type = db.Column(db.Enum(FileType), nullable=False)
    material = db.Column(db.Enum(Material), nullable=False)

    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    business = db.relationship('BusinessModel', back_populates='printer')

    def __init__(self, business_id: int, **kwargs):
        super(PrinterModel, self).__init__(**kwargs)
        self.business_id = business_id

    def __repr__(self):
        return f'<PrinterModel name: {self.name}, model: {self.model}, width: {self.base_width}, ' \
               f'length: {self.base_length}, height: {self.height}, file_type: {self.file_type}, material: ' \
               f'{self.material}>'

    @classmethod
    def find_printer_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_printer_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_printer_by_name_and_business_id(cls, name, business_id):
        return cls.query.filter_by(business_id=business_id, name=name).first()

    @classmethod
    def list_printers_by_business_id(cls, business_id):
        return cls.query.filter_by(business_id=business_id).all()

    @property
    def printer_build_volume(self):
        """Computes and returns the volume of the build area in cubic millimeters"""
        return self.base_length * self.base_width * self.height

    def save_printer_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_printer_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update_printer_in_db():
        db.session.commit()

    @staticmethod
    def rollback_printer_changes():
        """Roll back changes in the current session"""
        db.session.rollback()
