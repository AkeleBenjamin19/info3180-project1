from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,FileField,TextAreaField,SelectField
from wtforms.validators import InputRequired, DataRequired


class PropertyForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    numberOfBedrooms = IntegerField('No. of Rooms', validators=[DataRequired()])
    numberOfBathrooms = IntegerField('No. of Bathrooms', validators=[DataRequired()])
    price = IntegerField('Price', validators=[InputRequired()])
    type = SelectField('Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[DataRequired()])
    location = StringField('Location', validators=[InputRequired()])
    description= TextAreaField('Description', validators=[DataRequired()])
    filename=FileField('Photo',validators=[DataRequired()])

