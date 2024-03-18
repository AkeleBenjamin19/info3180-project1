from . import db
from enum import Enum

class PropertyType(Enum):
    House = 'House'
    Apartment = 'Apartment'


class Property(db.Model):
    __tablename__ = 'property_tb'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    numberOfBedrooms = db.Column(db.Integer)
    numberOfBathrooms = db.Column(db.Integer)
    location= db.Column(db.String(255))
    price= db.Column(db.Integer)
    type = db.Column(db.Enum(PropertyType))
    description = db.Column(db.Text)
    filename=db.Column(db.String(255))


    def __init__(self, title,numberOfBedrooms,numberOfBathrooms,location,price,type,description,filename):
        self.title = title
        self.numberOfBedrooms = numberOfBedrooms
        self.numberOfBathrooms = numberOfBathrooms
        self.location = location
        self.price = price
        self.type=type
        self.description=description
        self.filename=filename

        

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

