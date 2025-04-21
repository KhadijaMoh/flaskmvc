from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField, SelectMultipleField, widgets
from wtforms.validators import DataRequired

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class ApartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    amenities = MultiCheckboxField('Amenities', choices=[
        ('pool', 'Pool'),
        ('gym', 'Gym'),
        ('parking', 'Parking'),
        ('balcony', 'Balcony'),
        ('laundry', 'In-unit Laundry'),
        ('pet-friendly', 'Pet-Friendly'),
        # Add more amenities as needed
    ])
    price = FloatField('Price', validators=[DataRequired()])
    submit = SubmitField('Save Apartment')