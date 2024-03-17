from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,FileField
from wtforms.validators import InputRequired, Email

class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    numberOfBedrooms = IntegerField('No. of Rooms', validators=[InputRequired()])
    numberOfBathrooms = IntegerField('No. of Bathrooms', validators=[InputRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    type = StringField('Property Type', validators=[InputRequired()])
    location = StringField('Location', validators=[InputRequired()])
    filename=FileField('Photo',)